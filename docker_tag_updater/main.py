"""The main library."""

import json
import shutil
import subprocess
from typing import Callable, Never, Optional

import semver

from .helpers import RegexRules, parse_version, rules


def check_skopeo() -> None:
    """Check if the system has skopeo installed."""
    if not shutil.which("skopeo"):
        raise SystemError(
            "skopeo needs to be installed. Refer to "
            "https://github.com/containers/skopeo/blob/main/install.md "
            "for more information."
        )


def failed_skopeo_response(
    image: str, registry: str, base_tag: str, exc: Exception = ValueError()
) -> Never:
    raise ValueError(
        f"The skopeo response for {registry}/{image}:{base_tag} is invalid."
    ) from exc


def skopeo_inspect(
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
            failed_skopeo_response(image, registry, base_tag)
        return json_response
    except subprocess.CalledProcessError as exc:
        failed_skopeo_response(image, registry, base_tag, exc)


def get_newest_version_label(
    image: str,
    registry: str = "docker.io",
    base_tag: str = "latest",
    inspector: Callable = skopeo_inspect,
) -> str:
    """Get the container image version from its annotations."""
    inspect_resp = inspector(image, registry, base_tag)
    try:
        return inspect_resp["config"]["Labels"]["org.opencontainers.image.version"]
    except KeyError as exc:
        raise KeyError(
            f"The version label for {registry}/{image}:{base_tag} is not set."
        ) from exc


def compare_image_versions(
    cur_ver: str,
    new_ver: str,
    registry: str,
    regex_rules: RegexRules = rules,
    strict: bool = False,
) -> Optional[str]:
    """Compare the current and newest semver, return the newest version."""
    if cur_ver == new_ver:
        return None

    cur_semver = parse_version(cur_ver, regex_rules, registry)
    new_semver = parse_version(new_ver, regex_rules, registry)

    if semver.compare(new_semver, cur_semver) > 0:
        return new_ver
    return None
