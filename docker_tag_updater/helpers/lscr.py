"""lscrRules RegexRules object."""

from .regex_rules import RegexRules

lscrRules = RegexRules(
    rules={
        "lscr": r"v?(?:ersion-)?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
        r"(?:\.(?P<prerelease>\d+))?(?:-ls(?P<build>\d+))?",
    }
)
"""The RegexRule object for parsing linuxserver container semantic versions.

This object has the following equivalent aliases: lscr, lscr.io, and lxs.
"""

lscrRules.add_alias("lscr", "lscr.io", "linuxserver", "lxs")
