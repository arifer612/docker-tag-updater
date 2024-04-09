"""The command line parser module."""

import argparse


ciu_parser = argparse.ArgumentParser(
    prog="Compose Image Updater",
    description="Check for updates to your Docker images' version tags.",
)

ciu_parser.add_argument(
    "image",
    help="""The name of the image that will be checked.
    Example: docker.io/alpine:3.19.1
    """)
ciu_parser.add_argument(
    "-t",
    "--tag",
    help="The base tag to reference, e.g. latest, develop, alpine, etc.",
    default="latest",
)
ciu_parser.add_argument(
    "-r",
    "--rule",
    choices=["default", "lscr"],
    help="The semver regex rule.",
    default="default",
)
ciu_parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
)
