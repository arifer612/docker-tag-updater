"""A set of helpers."""

import re

from .regex_rules import DefaultRules, RegexRules


def parse_version(
    ver: str, regex_rules: RegexRules = DefaultRules, rule: str = "default"
) -> str:
    """Parse the version according to a regex rule."""
    if not regex_rules.has_rule(rule):
        raise KeyError(f"{rule} is not a valid regex rule.")
    raw_pattern = (
        regex_rules[rule]["raw_pattern"] or regex_rules["default"]["raw_pattern"]
    )
    replacement = (
        regex_rules[rule]["replacement"] or regex_rules["default"]["replacement"]
    )
    return re.sub(raw_pattern, replacement, ver)
