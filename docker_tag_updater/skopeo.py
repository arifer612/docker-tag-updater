"""Tools for Skopeo."""

import json
import subprocess
from typing import Callable, Never

import semver

from .helpers import parse_version


def _failed_response(
    image: str, registry: str, base_tag: str, exc: Exception = ValueError()
) -> Never:
    """Handle a failed Skopeo response.

    Parameters
    ----------
    image
        The name of the container image.
    registry
        The registry hosting the container image.
    base_tag
        The tag of the container image.
    exc
        The Exeception that caught the failed response.

    Raises
    ------
    ValueError
        Handles any caught exceptions and raises it as a ValueError for the user to
        troubleshoot or debug if need be.

    """
    raise ValueError(
        f"The skopeo response for {registry}/{image}:{base_tag} is invalid."
    ) from exc


def parse(image_string: str) -> tuple[str, str, str]:
    """Parse the image string to get its registry, image, and tag.

    Parameters
    ----------
    image_string
        The container image possibly with the registry and tag included.

    Returns
    -------
    tuple of str
        The registry, image, and tag as a tuple.

    Examples
    --------
    >>> _parse('hello-world')
    ('docker.io', 'hello-world', 'latest')

    >>> _parse('lscr.io/linuxserver/mariadb:10.11.6-r0-ls136')
    ('lscr.io', 'linuxserver/mariadb', '10.11.6-r0-ls136')

    """
    if ":" in image_string:
        image_string, tag = image_string.split(":", 1)
    else:
        tag = "0"
    if (image_string.count("/") > 1) or ".io" in image_string:
        registry, *image_string_list = image_string.split("/")
        image_string = "/".join(image_string_list)
    else:
        registry = "docker.io"
    return (registry, image_string, tag)


def inspect(
    image: str,
    registry: str = "docker.io",
    base_tag: str = "latest",
    verbose: bool = False,
) -> dict:
    """Run 'skopeo inspect'.

    A container image will be queried by skopeo and the contents of the inspection will
    be returned as a dictionary as-is.

    Parameters
    ----------
    image
        The name of the container image.
    registry
        The registry hosting the container image.
    base_tag
        The tag of the container image.
    verbose
        Print out the error messages from the skopeo process to STDERR if True.

    Returns
    -------
    dict
        The result of the skopeo process as a dictionary.

    """
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
            _failed_response(image, registry, base_tag)
        return json_response
    except subprocess.CalledProcessError as exc:
        _failed_response(image, registry, base_tag, exc)


def image_version(
    image: str,
    registry: str = "docker.io",
    base_tag: str = "latest",
    inspector: Callable = inspect,
    verbose: bool = False,
) -> str:
    """Get the container image version from its annotations.

    Parameters
    ----------
    image
        The container image, e.g., hello-world.
    registry
        The registry where the image is hosted on.
    base_tag
        The name of the base tag to refer against.
    inspector
        The inspection method.
    verbose
        Specify the verbosity of the inspector function.

    Returns
    -------
        The most up-to-date version of the image with the specified tag on the
        specified registry.

    Raises
    ------
    KeyError
        If annotations of the container image is not set.

    Examples
    --------
    The current tagged version of traefik is v2.11.0. This is also reflected in
    their annotated Docker container image.

    >>> image_version("traefik")
    v2.11.0

    On the other hand, the official hello-world Docker container image does not
    have the right annotations. It will raise a KeyError.

    >>> image_version("hello-world")
    KeyError: 'The version label for docker.io/hello-world:latest is not set.'

    """
    if verbose:
        print(f"Inspecting {image} tagged with {base_tag} on {registry}")

    inspect_resp = inspector(image, registry, base_tag, verbose)
    try:
        version = inspect_resp["config"]["Labels"]["org.opencontainers.image.version"]
        if verbose:
            print(f"The latest version of {base_tag} for {image} is {version}.")
        return version
    except KeyError as exc:
        raise KeyError(
            f"The version label for {registry}/{image}:{base_tag} is not set."
        ) from exc


def compare_versions(
    source_ver: str,
    target_ver: str,
    rule: str = "default",
    strict: bool = False,
    verbose: bool = False,
) -> str:
    """Compare the current and newest semver, return the neweset version.

    The comparision will be done using the python-semver package. A simple comparison of
    the major, minor, and patch versions only, is implemented in this version.

    Parameters
    ----------
    source_ver
        The semver string of the source.
    target_ver
        The semver string of the target.
    rule
        Name of the helpers.RegexRules to parse these semver strings.
    strict
        (Currently unimplemented)
    verbose
        Specify the verbosity of the inspector function.

    Returns
    -------
        The most up-to-date semver string.

    Examples
    --------
    >>> compare_versions("v1.2.3", "v1.2.4", rule="default")
    v1.2.4

    >>> compare_versions("v1.2.4", "v1.2.3", rule="default")
    v1.2.4

    Comparing linuxserver semver strings will only consider up to its patch version.

    >>> compare_versions("v1.2.3.456-ls789", "v1.2.3.456-ls798", rule="lscr")
    v1.2.3.456-ls789

    """
    if verbose:
        print(f"Comparing {source_ver} against {target_ver}...")

    if source_ver == target_ver:
        return source_ver

    source_semver = parse_version(source_ver, rule_name=rule)
    target_semver = parse_version(target_ver, rule_name=rule)

    if semver.Version(**target_semver) > semver.Version(**source_semver):
        return target_ver
    return source_ver
