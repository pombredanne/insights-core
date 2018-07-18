"""
Subscription manager release commands
=====================================

Shared parser for parsing output of the ``subscription-manager release``
commands.

SubscriptionManagerReleaseShow - command ``subscription-manager release --show``
--------------------------------------------------------------------------------

"""
from .. import parser, CommandParser
from insights.parsers import SkipException
from insights.specs import Specs


@parser(Specs.subscription_manager_release_show)
class SubscriptionManagerReleaseShow(CommandParser):
    """
    Class for parsing the output of `subscription-manager release --show` command.

    Typical output of the command is::

        Release: 7.2

    Attributes:
        set (str): the set release.
        major (int): the major version of the set release.
        minor (int): the minor version of the set release.

    Examples:
        >>> type(rhsm_rel)
        <class 'insights.parsers.subscription_manager_release.SubscriptionManagerReleaseShow'>
        >>> rhsm_rel.set
        '7.2'
        >>> rhsm_rel.major
        7
        >>> rhsm_rel.minor
        2
    """

    def parse_content(self, content):
        self.set = self.major = self.minor = None
        l = len(content)
        if l != 1:
            raise SkipException("Content takes at most 1 line ({0} given).".format(l))
        line = content[0].strip()
        if line != 'Release not set':
            line_splits = line.split()
            if len(line_splits) == 2:
                rel = line_splits[-1]
                rel_splits = rel.split('.')
                if (len(rel_splits) == 2 and rel_splits[0].isdigit() and
                        rel_splits[-1].isdigit()):
                    self.set = rel
                    self.major = int(rel_splits[0])
                    self.minor = int(rel_splits[-1])
                    return
            raise SkipException("Incorrect content: {0}".format(line))
