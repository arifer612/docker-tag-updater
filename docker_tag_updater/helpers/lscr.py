"""Linuxserver regex rules."""

from .regex_rules import RegexRules

lscrRules = RegexRules(
    {
        "lscr": {
            "raw_pattern":
            r"v?(?:ersion-)?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:\.(?P<prerelease>\d+))?(?:-ls(?P<build>\d+))?",
            "replacement": r"\g<maj>.\g<min>.\g<pat>-\g<rel>+\g<bld>",
        },
    }
)
lscrRules.add_alias("lscr", "lscr.io", "linuxserver", "lxs")
