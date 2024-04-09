"""Dictionary object for version parsing using regex.

This module defines the most fundamental object that is used by all other modules of
this subpackage.
"""
from __future__ import annotations


class RegexRules(dict):
    """An aliased dictionary with defined regex rules for version parsing.

    Parameters
    ----------
    rules:
        A dictionary containing names as keys and regex strings as values.

    Examples
    --------
    The DefaultRules object that is provided in this module is created as follows.

    >>> DefaultRules = RegexRules(
    ...     rules = {
    ...         "default": r"v?(?:ersion-)?(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+).*",
    ...     }
    ... )

    Notes
    -----
    RegexRules objects can be added together to concatenate into a larger
    RegexRules object. Do take note that a new rule is always prioritised over an
    existing rule with the same name, i.e., the operation does not always commute.

    See Also
    --------
    DefaultRules : For an example of a RegexRules object.
    """

    def __init__(self, rules: dict[str, str]):
        dict.__init__(self, **rules)
        self._rule_aliases = {}

    def __getitem__(self, rule):
        return dict.__getitem__(self, self._rule_aliases.get(rule, rule))

    def __setitem__(self, rule, value):
        return dict.__setitem__(self, self._rule_aliases.get(rule, rule), value)

    def __repr__(self):
        return f"RegexRules[{' '.join([rule for rule in self.keys()])}]"

    def get(self, rule: str) -> str:
        """Redefine the get function.

        Parameters
        ----------
        rule
            The name of the rule or its alias.

        Returns
        -------
            A regex raw string.

        Examples
        --------
        >>> rules.get('default')
        'v?(?:ersion-)?(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+).*'
        """
        return self.__getitem__(rule)

    def has_rule(self, rule: str) -> bool:
        """Check if the rule exists or is an alias.

        Parameters
        ----------
        rule:
            The name of the rule to check its existence of.

        Returns
        -------
            True if the rule exists as either a real rule or an alias in this
            RegexRules object, and False otherwise.
        """
        return (rule in self.keys()) or (rule in self._rule_aliases)

    def __add__(self, other_rules: RegexRules) -> RegexRules:
        ### for existing rule key, new rule takes precedence.
        """The internal addition operator

        A new rule is prioritised over an existing rule with the same name.

        Parameters
        ----------
        other_rules:
            A different set of RegexRules.

        Returns
        -------
            A RegexRules object that is not smaller than the original size

        Examples
        --------
        Adding lscr.lscrRules to defaultRules will produce a RegexRules with 2 rules.
        >>> defaultRules + lscrRules
        {
            'default': 'v?(?:ersion-)?(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+).*',
            'lscr': 'v?(?:ersion-)?(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+)(?:\\.(?P<prerelease>\\d+))?(?:-ls(?P<build>\\d+))?',
        }

        Adding a RegexRules with the same name produces a RegexRules with only
        1 rule.
        >>> NewRules = RegexRules(
        ...    rules = {
        ...        "default": r"(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+).*",
        ...    }
        ...)
        >>> DefaultRules + NewRules
        {"default": r"(?P<major>\\d+)\\.(?P<minor>\\d+)\\.(?P<patch>\\d+).*"}
        """
        new_rule = RegexRules(rules=self)
        new_rule._rule_aliases.update(self._rule_aliases)
        new_rule.update(other_rules)
        new_rule._rule_aliases.update(other_rules._rule_aliases)
        return new_rule

    def add_alias(self, main_rule: str, *aliases: str) -> None:
        """Add a number of aliases to the rule.

        Parameters
        ----------
        main_rule:
            The name main rule to add aliases to.
        aliases:
            Strings of aliases to the main rule.

        Examples
        --------
        To add the aliases "docker.io" and "docker" to the rule named
        "default", do the following:
        >>> DefaultRules.add_alias("default", "docker.io", "docker")

        Raises
        ------
        NotImplementedError
            If there are no aliases to be added.
        """
        if len(aliases) == 0:
            raise NotImplementedError(f"Aliases for {main_rule} are not declared.")
        for alias in aliases:
            self._rule_aliases[alias] = main_rule


DefaultRules = RegexRules(
    rules = {
        "default": r"v?(?:ersion-)?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+).*",
    }
)
"""The default rule that should work for most standard semantic versions.

This object has the following equivalent aliases: default, docker.io, and docker.
"""

DefaultRules.add_alias("default", "docker.io", "docker")
