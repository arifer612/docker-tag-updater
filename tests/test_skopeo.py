import pytest

from docker_tag_updater import skopeo

baseimage_alpine_tag = "3.18-f7e3c236-ls38"


def test_valid_inspect():
  """Test a valid inspect call.

  Run skopeo inspect for linuxserver/baseimage-alpine hosted on ghcr.io, where
  the base tag is specificied in baseimage_alpine_tag.

  """
  assert isinstance(
        skopeo.inspect(
            "linuxserver/baseimage-alpine", "ghcr.io", baseimage_alpine_tag
        ),
        dict
    )

def test_inspect_invalid_registry():
  "Test inspect with an invalid registry."
  with pytest.raises(ValueError):
    skopeo.inspect("linuxserver/baseimage-alpine", "xxxx", baseimage_alpine_tag)


def test_inspect_inavlid_image():
  "Test inspect with an invalid image."
  with pytest.raises(ValueError):
    skopeo.inspect("linuxserver/asdlkasdf", "ghcr.io", baseimage_alpine_tag)

def test_inspect_invalid_tag():
  "Test inspect with an invalid base tag."
  with pytest.raises(ValueError):
    skopeo.inspect("linuxserver/baseimage-alpine", "ghcr.io", "asdf")
