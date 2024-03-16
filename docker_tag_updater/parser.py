"""The command line parser module."""

import argparse


ciu_parser = argparse.ArgumentParser(
    prog="Compose Image Updater",
    description="Check for updates to your Docker images' version tags.",
)

subparsers = ciu_parser.add_subparsers(required=True, dest='command')
skopeo_parser = subparsers.add_parser(
    "inspect", aliases=["i"], help="Inspect using Skopeo."
)
skopeo_parser.add_argument("image", help="The name of the image that will be checked.")
skopeo_parser.add_argument(
    "-t", "--tag", help="The base tag to reference, e.g. latest, develop, alpine, etc."
)

compare_parser = subparsers.add_parser(
    "compare", aliases=["c"], help="Compare the semver."
)
compare_parser.add_argument(
    "current", help="The current image string from the compose.yaml."
)
compare_parser.add_argument("newest", help="The newest image version (ciu skopeo).")
compare_parser.add_argument(
    "-r",
    "--rule",
    choices=["default", "lscr"],
    help="The semver regex rule.",
    default="default",
)
