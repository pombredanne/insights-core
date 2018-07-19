import sys
import os
import pytest
import subprocess
import shlex
import requests

from insights.client import InsightsClient
from insights.client.config import InsightsConfig
from insights import package_info
from insights.client.auto_config import try_auto_configuration
from insights.client.constants import InsightsConstants as constants
# from insights.client.utilities import delete_registered_file, write_to_disk


def test_version():

    # Hack to prevent client from parsing args to py.test
    tmp = sys.argv
    sys.argv = []

    try:
        config = InsightsConfig(logging_file='/tmp/insights.log')
        client = InsightsClient(config)
        result = client.version()
        assert result == "%s-%s" % (package_info["VERSION"], package_info["RELEASE"])
    finally:
        sys.argv = tmp


def test_register():
    config = InsightsConfig(register=True)
    client = InsightsClient(config)
    try_auto_configuration(config)
    assert client.unregister() is True
    assert client.register() is True
    for r in constants.registered_files:
        assert os.path.isfile(r) is True
    for u in constants.unregistered_files:
        assert os.path.isfile(u) is False


def test_unregister():
    config = InsightsConfig(unregister=True)
    client = InsightsClient(config)
    try_auto_configuration(config)
    assert client.unregister() is True
    for r in constants.registered_files:
        assert os.path.isfile(r) is False
    for u in constants.unregistered_files:
        assert os.path.isfile(u) is True


def test_force_reregister():
    config = InsightsConfig(reregister=True)
    client = InsightsClient(config)
    try_auto_configuration(config)

    # initialize comparisons
    old_machine_id = None
    new_machine_id = None

    # register first
    assert client.register() is True
    for r in constants.registered_files:
        assert os.path.isfile(r) is True

    # get modified time of .registered to ensure it's regenerated
    old_reg_file1_ts = os.path.getmtime(constants.registered_files[0])
    old_reg_file2_ts = os.path.getmtime(constants.registered_files[1])

    with open(constants.machine_id_file) as mid:
        old_machine_id = mid.read()

    # reregister with new machine-id
    config.reregister = True
    assert client.register() is True

    with open(constants.machine_id_file) as mid:
        new_machine_id = mid.read()
    new_reg_file1_ts = os.path.getmtime(constants.registered_files[0])
    new_reg_file2_ts = os.path.getmtime(constants.registered_files[1])

    assert old_machine_id != new_machine_id
    assert old_reg_file1_ts != new_reg_file1_ts
    assert old_reg_file2_ts != new_reg_file2_ts


def test_register_container():
    with pytest.raises(ValueError):
        InsightsConfig(register=True, analyze_container=True)


def test_unregister_container():
    with pytest.raises(ValueError):
        InsightsConfig(unregister=True, analyze_container=True)


def test_force_reregister_container():
    with pytest.raises(ValueError):
        InsightsConfig(reregister=True, analyze_container=True)


def test_reg_check_registered():
    # register the machine first
    config = InsightsConfig(register=True)
    client = InsightsClient(config)
    try_auto_configuration(config)
    assert client.register() is True
    config.register = False

    # test function and integration in .register()
    assert client.get_registration_information()['status'] is True
    assert client.register() is True
    for r in constants.registered_files:
        assert os.path.isfile(r) is True
    for u in constants.unregistered_files:
        assert os.path.isfile(u) is False


def test_reg_check_unregistered():
    # unregister the machine first
    config = InsightsConfig(unregister=True)
    client = InsightsClient(config)
    try_auto_configuration(config)
    assert client.unregister() is True
    config.unregister = False

    # test function and integration in .register()
    assert client.get_registration_information()['status'] is False
    assert client.register() is False
    for r in constants.registered_files:
        assert os.path.isfile(r) is False
    for u in constants.unregistered_files:
        assert os.path.isfile(u) is True


def test_reg_check_registered_unreachable():
    # register the machine first
    config = InsightsConfig(register=True)
    client = InsightsClient(config)
    try_auto_configuration(config)
    assert client.register() is True
    config.register = False
    config.http_timeout = 1

    # set net delay and try to check registration
    subprocess.call(
        shlex.split('tc qdisc add dev eth0 root netem delay 1001ms'))
    with pytest.raises(requests.exceptions.Timeout):
        assert client.get_registration_information()['unreachable'] is True
        assert client.register() is None
    subprocess.call(
        shlex.split('tc qdisc del dev eth0 root netem delay 1001ms'))
    for r in constants.registered_files:
        assert os.path.isfile(r) is True
    for u in constants.unregistered_files:
        assert os.path.isfile(u) is False


def test_reg_check_unregistered_unreachable():
    # unregister the machine first
    config = InsightsConfig(unregister=True)
    client = InsightsClient(config)
    try_auto_configuration(config)
    assert client.unregister() is True
    config.unregister = False
    config.http_timeout = 1

    # set net delay and try to check registration
    subprocess.call(
        shlex.split('tc qdisc add dev eth0 root netem delay 1001ms'))
    with pytest.raises(requests.exceptions.Timeout):
        assert client.get_registration_information()['unreachable'] is True
        assert client.register() is None
    subprocess.call(
        shlex.split('tc qdisc del dev eth0 root netem delay 1001ms'))
    for r in constants.registered_files:
        assert os.path.isfile(r) is False
    for u in constants.unregistered_files:
        assert os.path.isfile(u) is True
