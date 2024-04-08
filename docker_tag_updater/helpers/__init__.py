"""A set of helpers."""

import re

from .lscr import lscrRules
from .regex_rules import DefaultRules, RegexRules
from typing import Any


def parse_version(
    version: str, rules: RegexRules = DefaultRules, rule_name: str = "default"
) -> dict[str, Any]:
    """Parse the version according to a regex rule.

    Parameters
    ----------
    version:
        A semver string.
    rules:
        A set of RegexRules.
    rule_name:
        The name of the rule, or its alias.

    Returns
    -------
        A dictionary that can be parsed by python-semver.

    Raises
    ------
    KeyError
        If rule_name is not the name or alias of a rule in the rules RegexRules object.
    ValueError
        If there the version cannot be parsed by either the specified rule or
        the default rule.

    Examples
    --------
    >>> parse_version('v1.2.3')
    {'major': '1', 'minor': '2', 'patch': '3'}

    >>> parse_version("v1.2.3.456-ls789", regex_rules=lscrRules, rule="lscr")
    {'major': '1', 'minor': '2', 'patch': '3', 'prerelease': '456', 'build': '789'}

    See Also
    --------
    regex_rules.RegexRules
    """
    if not rules.has_rule(rule_name):
        raise KeyError(f"{rule_name} is not a valid rule or does not exist as a rule.")
    rule_rx = rules[rule_name]
    match_pattern = re.fullmatch(rule_rx, version)
    if match_pattern:
        return match_pattern.groupdict("0")
    if rule_name != "default":
        # Try with the default rule if all else fails
        return parse_version(version, rules, "default")
    raise ValueError(f"The {rule_name} rule cannot parse the version string {version}.")


rules = DefaultRules + lscrRules
