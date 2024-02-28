import pytest

from docker_tag_updater import main

baseimage_alpine_tag = "3.18-f7e3c236-ls38"


def test_valid_skopeo_inspect():
  """Test a valid skopeo_inspect call.

  Run skopeo inspect for linuxserver/baseimage-alpine hosted on ghcr.io, where
  the base tag is specificied in baseimage_alpine_tag.

  """
  assert isinstance(
        main.skopeo_inspect(
            "linuxserver/baseimage-alpine", "ghcr.io", baseimage_alpine_tag
        ),
        dict
    )

def test_skopeo_inspect_invalid_registry():
  "Test skopeo_inspect with an invalid registry."
  with pytest.raises(ValueError):
    main.skopeo_inspect("linuxserver/baseimage-alpine", "xxxx", baseimage_alpine_tag)


def test_skopeo_inspect_inavlid_image():
  "Test skopeo_inspect with an invalid image."
  with pytest.raises(ValueError):
    main.skopeo_inspect("linuxserver/asdlkasdf", "ghcr.io", baseimage_alpine_tag)

def test_skopeo_inspect_invalid_tag():
  "Test skopeo_inspect with an invalid base tag."
  with pytest.raises(ValueError):
    main.skopeo_inspect("linuxserver/baseimage-alpine", "ghcr.io", "asdf")
