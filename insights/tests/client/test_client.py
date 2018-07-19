import sys
import os
import pytest
import subprocess
import shlex

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
    config = InsightsConfig()
    client = InsightsClient(config)
    try_auto_configuration(config)
    assert client.register() is True
    assert client.get_registration_information()['is_registered'] is True
    for r in constants.registered_files:
        assert os.path.isfile(r) is True
    for u in constants.unregistered_files:
        assert os.path.isfile(u) is False


def test_reg_check_unregistered():
    config = InsightsConfig()
    client = InsightsClient(config)
    try_auto_configuration(config)
    assert client.unregister() is True
    assert client.get_registration_information()['is_registered'] is False
    for r in constants.registered_files:
        assert os.path.isfile(r) is False
    for u in constants.unregistered_files:
        assert os.path.isfile(u) is True


def test_reg_check_registered_unreachable():
    config = InsightsConfig(http_timeout=1)
    client = InsightsClient(config)
    try_auto_configuration(config)
    assert client.register() is True
    subprocess.run(
        shlex.split('tc qdisc add dev eth0 root netem delay 1001ms'))
    assert client.get_registration_information()['unreachable'] is True
    assert client.register() is None
    subprocess.run(shlex.split('tc qdisc del dev eth0 root netem delay 1001ms'))
    for r in constants.registered_files:
        assert os.path.isfile(r) is True
    for u in constants.unregistered_files:
        assert os.path.isfile(u) is False


def test_reg_check_unregistered_unreachable():
    config = InsightsConfig(http_timeout=1)
    client = InsightsClient(config)
    try_auto_configuration(config)
    assert client.unregister() is True
    subprocess.run(
        shlex.split('tc qdisc add dev eth0 root netem delay 1001ms'))
    assert client.get_registration_information()['unreachable'] is True
    assert client.register() is None
    subprocess.run(
        shlex.split('tc qdisc del dev eth0 root netem delay 1001ms'))
    for r in constants.registered_files:
        assert os.path.isfile(r) is False
    for u in constants.unregistered_files:
        assert os.path.isfile(u) is True
