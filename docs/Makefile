SPHINXOPTS  ?= "-W"
SPHINXBUILD ?= sphinx-build
SPHINXAPI   ?= sphinx-apidoc
SOURCEDIR   = source
BUILDDIR    = build
APIDOCDIR   = "${SOURCEDIR}/api"
MODULE      = $(shell cat ../pyproject.toml | grep package_root | cut -d \" -f 2)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

clear_autodocs:
	@[ -d "${APIDOCDIR}" ] && \
	rm -rf "${APIDOCDIR}" || \
	true

rebuild: clear_autodocs
	@$(SPHINXAPI) -o "${APIDOCDIR}" "../${MODULE}" \
	--separate \
	--templatedir "${SOURCEDIR}/_templates"

clean: Makefile
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html: Makefile
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: docs
docs: clean rebuild html

.PHONY: read
read: docs
	@xdg-open "${BUILDDIR}/html/index.html"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
