from insights.parsers import SkipException, subscription_manager_release
from insights.parsers.subscription_manager_release import SubscriptionManagerReleaseShow
from insights.tests import context_wrap
import pytest
import doctest

INPUT_NORMAL = """
Release: 7.2
""".strip()

INPUT_NO_SET = """
Release not set
""".strip()

INPUT_NG_1 = """
XYC
Release not set
""".strip()

INPUT_NG_2 = """
Release: '7.x'
""".strip()


def test_subscription_manager_release_show_ok():
    ret = SubscriptionManagerReleaseShow(context_wrap(INPUT_NORMAL))
    assert ret.set == '7.2'
    assert ret.major == 7
    assert ret.minor == 2


def test_subscription_manager_release_show_not_set():
    with pytest.raises(SkipException) as e_info:
        SubscriptionManagerReleaseShow(context_wrap(INPUT_NO_SET))
    assert "Incorrect content: Release not set" in str(e_info.value)


def test_subscription_manager_release_show_ng():
    with pytest.raises(SkipException) as e_info:
        SubscriptionManagerReleaseShow(context_wrap(INPUT_NG_1))
    assert "Incorrect content: XYC" in str(e_info.value)

    with pytest.raises(SkipException) as e_info:
        SubscriptionManagerReleaseShow(context_wrap(INPUT_NG_2))
    assert "Incorrect content: Release: '7.x'" in str(e_info.value)


def test_doc_examples():
    env = {
            'rhsm_rel': SubscriptionManagerReleaseShow(context_wrap(INPUT_NORMAL)),
          }
    failed, total = doctest.testmod(subscription_manager_release, globs=env)
    assert failed == 0