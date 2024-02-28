"""Linuxserver regex rules."""

from .regex_rules import RegexRules

lscrRules = RegexRules(
    {
        "lscr": {
            "raw_pattern": r"(\d+)\.(\d+)\.(\d+)\.(\d+)-(.*)",
            "replacement": r"\1.\2.\3-\4+\5",
        },
    }
)
lscrRules.add_alias("lscr", "lscr.io", "linuxserver", "lxs")
