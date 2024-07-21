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


def test_yymmdd_parser_standard():
    """Parse a standard YYMMDD version string with the yymmdd rule."""
    vstring = "24.06.01"
    assert helpers.parse_version(vstring, helpers.rules, "yymmdd") == {
        "major": "24",
        "minor": "06",
        "patch": "01",
    }

def test_yymmdd_parser_longstring():
    """Parse a standard YYYYMMDD version string with the yymmdd rule."""
    vstring = "20240601"
    assert helpers.parse_version(vstring, helpers.rules, "yymmdd") == {
        "major": "24",
        "minor": "06",
        "patch": "01",
    }

def test_yymmdd_parser_invalid_string_length():
    """Parse an invalid MMDD version string with the yymmdd rule."""
    vstring = "0601"
    with pytest.raises(ValueError):
        helpers.parse_version(vstring, helpers.rules, "yymmdd")

def test_yymmdd_parser_semver_string():
    """Parse an semantic version string with the yymmdd rule."""
    vstring = "version-1.2.3-ls789"
    assert helpers.parse_version(vstring, helpers.rules, "yymmdd") == {
        "major": "1",
        "minor": "2",
        "patch": "3",
    }

def test_yyyymmdd_parser_standard():
    """Parse a standard YYYYMMDD version string with the yyyymmdd rule."""
    vstring = "20240601"
    assert helpers.parse_version(vstring, helpers.rules, "yyyymmdd") == {
        "major": "2024",
        "minor": "06",
        "patch": "01",
    }

def test_yyyymmdd_parser_longstring():
    """Parse a standard YYYYYYMMDD version string with the yyyymmdd rule."""
    vstring = "240601"
    with pytest.raises(ValueError):
        assert helpers.parse_version(vstring, helpers.rules, "yyyymmdd")

def test_yyyymmdd_parser_invalid_string_length():
    """Parse an invalid MMDD version string with the yyyymmdd rule."""
    vstring = "0601"
    with pytest.raises(ValueError):
        helpers.parse_version(vstring, helpers.rules, "yyyymmdd")

def test_yyyymmdd_parser_semver_string():
    """Parse an semantic version string with the yyyymmdd rule."""
    vstring = "version-1.2.3-ls789"
    assert helpers.parse_version(vstring, helpers.rules, "yyyymmdd") == {
        "major": "1",
        "minor": "2",
        "patch": "3",
    }
