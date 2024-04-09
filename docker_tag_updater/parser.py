"""The command line parser module.

This module defines the parser that is used for the CLI tool (image-version-checker).

"""

import argparse


ivc_parser = argparse.ArgumentParser(
    description="Check for updates to your Docker images' version tags.",
)
"""The argument parser for image-version-checker.

Parameters
----------
image : str
    The name of the container image, e.g., docker.io/alpine:3.19.1
tag : str, default: latest
    The base tag to compare the container image to, e.g., latest, edge, etc.
rule : str, default: default
    The rule used to parse the image tags/versions into a semantic version string for
    comparison. The available options now are (default, docker.io, docker, lscr,
    lscr.io, linuxserver)
verbose : bool, default: False
    Specify the verbosity of the inspector function.

See also
--------
docker_tag_updater.helpers.regex_rules : For more information about rules.

"""

ivc_parser.add_argument(
    "image",
    help="""The name of the image that will be checked.
    Example: docker.io/alpine:3.19.1
    """)
ivc_parser.add_argument(
    "-t",
    "--tag",
    help="The base tag to reference, e.g. latest, develop, alpine, etc.",
    default="latest",
)
ivc_parser.add_argument(
    "-r",
    "--rule",
    choices=["default", "lscr"],
    help="The semver regex rule.",
    default="default",
)
ivc_parser.add_argument(
    "-P",
    "--parse",
    action="store_true",
    help="Get the parsed image information, i.e., the registry, image name, and tag."
)
ivc_parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
)
