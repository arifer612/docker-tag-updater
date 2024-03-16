"""The default dictionary of regex rules for version parsing."""
from __future__ import annotations


class RegexRules(dict):
    """Aliased dictionary with regex rules for version parsing."""

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self._rule_aliases = {}

    def __getitem__(self, rule):
        return dict.__getitem__(self, self._rule_aliases.get(rule, rule))

    def __setitem__(self, rule, value):
        return dict.__setitem__(self, self._rule_aliases.get(rule, rule), value)

    def get(self, rule):
        """Redefine the get function."""
        return self.__getitem__(rule)

    def has_rule(self, rule) -> bool:
        """Check if the rule exists or is an alias."""
        if (rule in self.keys()) or (rule in self._rule_aliases):
            return True
        return False

    def __add__(self, other_rules: RegexRules) -> RegexRules:
        ### for existing rule key, new rule takes precedence.
        new_rule = RegexRules(**self)
        new_rule._rule_aliases.update(self._rule_aliases)
        new_rule.update(other_rules)
        new_rule._rule_aliases.update(other_rules._rule_aliases)
        return new_rule

    def add_alias(self, rule, *aliases):
        """Add a number of aliases to the rule."""
        if len(aliases) == 0:
            raise NotImplementedError(f"Aliases for {rule} are not declared.")
        for alias in aliases:
            self._rule_aliases[alias] = rule


DefaultRules = RegexRules(
    {
        "default": {
            "raw_pattern": r"v?(?:ersion-)?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+).*",
        }
    }
)
DefaultRules.add_alias("default", "docker.io", "docker")
