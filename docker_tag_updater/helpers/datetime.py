"""RegexRules object for datetime-like versions."""

from .regex_rules import RegexRules

yymmddRules: RegexRules = RegexRules(
    rules = {
        "yymmdd": r".*(?P<major>\d{2})(?P<minor>\d{2})(?P<patch>\d{2})"
    }
)
"""RegexRules for version strings of the type YYMMDD.

This object has the following equivalent aliases: yymmdd and YYMMDD.
"""

yymmddRules.add_alias("yymmdd", "YYMMDD")


yyyymmddRules: RegexRules = RegexRules(
    rules = {
        "yyyymmdd": r".*(?P<major>\d{4})(?P<minor>\d{2})(?P<patch>\d{2})"
    }
)
"""RegexRules for version strings of the type YYYYMMDD.

This object has the following equivalent aliases: yyyymmdd and YYYYMMDD.
"""

yyyymmddRules.add_alias("yyyymmdd", "YYYYMMDD")
