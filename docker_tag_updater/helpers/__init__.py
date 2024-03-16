"""A set of helpers."""

import re

from .lscr import lscrRules
from .regex_rules import DefaultRules, RegexRules
from typing import Any


def parse_version(
    ver: str, regex_rules: RegexRules = DefaultRules, rule: str = "default"
) -> dict[str, Any]:
    """Parse the version according to a regex rule."""
    if not regex_rules.has_rule(rule):
        raise KeyError(f"{rule} is not a valid regex rule.")
    raw_pattern = regex_rules[rule]["raw_pattern"]
    match_pattern = re.fullmatch(raw_pattern, ver)
    if match_pattern:
        return match_pattern.groupdict('0')
    if rule != "default":
        return parse_version(ver, regex_rules, 'default')
    raise ValueError(f"The {rule} rule cannot parse the version string {ver}.")


rules = DefaultRules + lscrRules
