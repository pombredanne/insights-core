import sys
import os

from insights.client import InsightsClient
from insights.client.config import InsightsConfig
from insights import package_info
from insights.client.auto_config import try_auto_configuration
from insights.client.constants import InsightsConstants as constants
from insights.client.utlities import delete_registered_file, write_to_disk


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
    delete_registered_file()
    # write_to_disk()
    config = InsightsConfig(register=True)
    client = InsightsClient(config)
    try_auto_configuration(config)
    # print(config)
    client.try_register()
    assert os.path.isfile('/etc/insights-client/.registered') is True


def test_unregister():
    config = InsightsConfig(unregister=True)


def test_force_reregister():
    config = InsightsConfig(reregister=True)


def test_register_offline():
    config = InsightsConfig(register=True, offline=True)
    # nothing should happen


def test_unregister_offline():
    config = InsightsConfig(unregister=True)
    # nothing should happen


def test_force_reregister_offline():
    config = InsightsConfig(reregister=True)
    # nothing should happen


def test_reg_check_registered():
    config = InsightsConfig()


def test_reg_check_unregistered():
    config = InsightsConfig()


def test_reg_check_unreachable():
    config = InsightsConfig()
