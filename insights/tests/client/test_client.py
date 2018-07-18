import sys

from insights.client import InsightsClient
from insights.client.config import InsightsConfig
from insights import package_info


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
