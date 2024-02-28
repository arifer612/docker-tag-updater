"""The main library."""

import json
import shutil
import subprocess
from typing import Callable


def check_skopeo() -> None:
    """Check if the system has skopeo installed."""
    if not shutil.which("skopeo"):
        raise SystemError(
            "skopeo needs to be installed. Refer to "
            "https://github.com/containers/skopeo/blob/main/install.md "
            "for more information."
        )


def skopeo_inspect(
    image: str, registry: str = "docker.io", base_tag: str = "latest"
) -> dict:
    "Run skopeo inspect."
    response = subprocess.run(
        ["skopeo", "inspect", "--config", f"docker://{registry}/{image}:{base_tag}"],
        stdout=subprocess.PIPE,
        check=True,
    )
    json_response = json.loads(response.stdout.decode())
    if not json_response:
        raise ValueError(
            f"The skopeo response for {registry}/{image}:{base_tag} is invalid."
        )
    return json_response


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
