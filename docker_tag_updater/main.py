"""The main library."""

import json
import shutil
import subprocess


def check_skopeo() -> None:
    """Check if the system has skopeo installed."""
    if not shutil.which("skopeo"):
        raise SystemError(
            "skopeo needs to be installed. Refer to "
            "https://github.com/containers/skopeo/blob/main/install.md "
            "for more information."
        )


def get_newest_version_label(
    image: str, registry: str = "docker.io", base_tag: str = "latest"
) -> str:
    """Get the most up-to-date version label of an image for the base tag."""
    inspect_response = subprocess.run(
        ["skopeo", "inspect", "--config", f"docker://{registry}/{image}:{base_tag}"],
        stdout=subprocess.PIPE,
        check=True,
    )
    inspect_dict = json.loads(inspect_response.stdout.decode())
    if not inspect_dict:
        raise ValueError(
            f"The skopeo response for {registry}/{image}:{base_tag} is invalid."
        )
    try:
        return inspect_dict["config"]["Labels"]["org.opencontainers.image.version"]
    except KeyError as exc:
        raise KeyError(
            f"The version label for {registry}/{image}:{base_tag} is not set."
        ) from exc
