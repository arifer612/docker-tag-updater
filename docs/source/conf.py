from sphinx_pyproject import SphinxConfig
import sys
import os

sys.path.insert(0, os.path.abspath('../../'))
config = SphinxConfig("../../pyproject.toml", globalns=globals(), style="poetry")
documentation_summary = config.description

# -- General configuration ---------------------------------------------------

extensions = config["extensions"]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}
