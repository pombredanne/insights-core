import sys
import os
import pytest

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


def test_register_offline():
    config = InsightsConfig(register=True, offline=True)
    # nothing should happen


def test_unregister_offline():
    config = InsightsConfig(unregister=True, offline=True)
    # nothing should happen


def test_force_reregister_offline():
    config = InsightsConfig(reregister=True, offline=True)
    # nothing should happen


def test_register_container():
    with pytest.raises(ValueError):
        config = InsightsConfig(register=True, analyze_container=True)


def test_unregister_container():
    with pytest.raises(ValueError):
        config = InsightsConfig(unregister=True, analyze_container=True)
        # nothing should happen


def test_force_reregister_container():
    with pytest.raises(ValueError):
        config = InsightsConfig(reregister=True, analyze_container=True)
        # nothing should happen


def test_reg_check_registered():
    config = InsightsConfig()


def test_reg_check_unregistered():
    config = InsightsConfig()


def test_reg_check_unreachable():
    config = InsightsConfig()
