from docker_tag_updater import helpers
import pytest


def test_invalid_rule():
    """Fail Parse an invalid regex rule."""
    with pytest.raises(KeyError):
        helpers.parse_version("", helpers.rules, "so-definitely-not-a-rule")


def test_invalid_string():
    """Fail to parse an invalid version string."""
    with pytest.raises(ValueError):
        helpers.parse_version("", helpers.rules, "default")


def test_lscr_parser_standard():
    """Parse a standard LSCR version string."""
    vstring = "v1.2.3.456-ls789"
    assert helpers.parse_version(vstring, helpers.rules, "lscr") == {
        "major": "1",
        "minor": "2",
        "patch": "3",
        "prerelease": "456",
        "build": "789",
    }


def test_lscr_parser_full():
    """Parse a full LSCR version string."""
    vstring = "version-1.2.3.456-ls789"
    assert helpers.parse_version(vstring, helpers.rules, "lscr") == {
        "major": "1",
        "minor": "2",
        "patch": "3",
        "prerelease": "456",
        "build": "789",
    }


def test_lscr_parser_no_prerelease():
    """Parse a LSCR version string without the prelease."""
    vstring = "version-1.2.3-ls789"
    assert helpers.parse_version(vstring, helpers.rules, "lscr") == {
        "major": "1",
        "minor": "2",
        "patch": "3",
        "prerelease": "0",
        "build": "789",
    }


def test_lscr_parser_no_build():
    """Parse a LSCR version string without the prelease."""
    vstring = "version-1.2.3.456"
    assert helpers.parse_version(vstring, helpers.rules, "lscr") == {
        "major": "1",
        "minor": "2",
        "patch": "3",
        "prerelease": "456",
        "build": "0",
    }


def test_lscr_parser_as_default():
    """Fall back to the default rule and parse an invalid LSCR version string."""
    vstring = "v1.2.3asdf"
    assert helpers.parse_version(vstring, helpers.rules, "lscr") == {
        "major": "1",
        "minor": "2",
        "patch": "3",
    }
