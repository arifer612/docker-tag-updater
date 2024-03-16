"""Tools for Skopeo."""

import json
import subprocess
from typing import Callable, Never, Optional

import semver

from .helpers import RegexRules, parse_version, rules


def failed_response(
    image: str, registry: str, base_tag: str, exc: Exception = ValueError()
) -> Never:
    raise ValueError(
        f"The skopeo response for {registry}/{image}:{base_tag} is invalid."
    ) from exc


def inspect(
    image: str,
    registry: str = "docker.io",
    base_tag: str = "latest",
    verbose: bool = False,
) -> dict:
    "Run skopeo inspect."
    try:
        response = subprocess.run(
            [
                "skopeo",
                "inspect",
                "--config",
                f"docker://{registry}/{image}:{base_tag}",
            ],
            stdout=subprocess.PIPE,
            stderr=None if verbose else subprocess.DEVNULL,
            check=True,
        )
        json_response = json.loads(response.stdout.decode())
        if not json_response:
            failed_response(image, registry, base_tag)
        return json_response
    except subprocess.CalledProcessError as exc:
        failed_response(image, registry, base_tag, exc)


def parse(image_string: str) -> tuple:
    """Parse the image string to get its registry, image, and tag."""
    if ":" in image_string:
        image_string, tag = image_string.split(':', 1)
    else:
        tag = '0'
    if image_string.count('/') > 1:
        registry, *image_string_list = image_string.split('/')
        image_string = '/'.join(image_string_list)
    else:
        registry = 'docker.io'
    return (registry, image_string, tag)


def image_version(
    image: str,
    registry: str = "docker.io",
    base_tag: str = "latest",
    inspector: Callable = inspect,
) -> str:
    """Get the container image version from its annotations."""
    inspect_resp = inspector(image, registry, base_tag)
    try:
        return inspect_resp["config"]["Labels"]["org.opencontainers.image.version"]
    except KeyError as exc:
        raise KeyError(
            f"The version label for {registry}/{image}:{base_tag} is not set."
        ) from exc


def compare_versions(
    cur_ver: str,
    new_ver: str,
    rule: str = 'default',
    strict: bool = False,
) -> str:
    """Compare the current and newest semver, return the newest version."""
    if cur_ver == new_ver:
        return cur_ver

    cur_semver = parse_version(cur_ver, rule=rule)
    new_semver = parse_version(new_ver, rule=rule)

    if semver.Version(**new_semver) > semver.Version(**cur_semver):
        return new_ver
    return cur_ver
