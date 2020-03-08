PACKAGE_NAME        = workflows.dsl
PACKAGE_DESCRIPTION = Python DSL for Argo Workflows

CURRENT_DIR ?= $(shell pwd)

define get_branch
$(shell git branch | sed -n '/\* /s///p')
endef

define get_tag
$(shell \
	if [ -z "`git status --porcelain`" ]; then \
		git describe \
			--exact-match \
			--tags HEAD 2>/dev/null || (>&2 echo "Tag has not been created.") \
	fi \
)
endef

define get_tree_state
$(shell \
	if [ -z "`git status --porcelain`" ]; then \
		echo "clean" \
	else \
		echo "dirty" \
	fi
)
endef

GIT_COMMIT     = $(shell git rev-parse HEAD)

GIT_BRANCH     = $(call get_branch)
GIT_TAG        = $(call get_tag)
GIT_TREE_STATE = $(call get_tree_state)

ifeq (${GIT_TAG},)
GIT_TAG = $(shell git rev-parse --abbrev-ref HEAD)
endif

VERSION    ?= $(shell b="${GIT_BRANCH}"; v="$${b/release-/}.0"; echo "$${v:0:5}")

PYPI_REPOSITORY ?= https://upload.pypi.org/legacy/


.PHONY: all
all:
	@echo "Nothing to do."


.PHONY: patch
patch: SHELL:=/bin/bash
patch: all
	- rm -rf build/ dist/
	- git tag --delete "v${VERSION}"

	$(MAKE) changelog

	sed -i "s/__version__ = \(.*\)/__version__ = \"${VERSION}\"/g" argo/workflows/dsl/__about__.py

	python setup.py sdist bdist_wheel
	twine check dist/* || (echo "Twine check did not pass. Aborting."; exit 1)

	git commit -a -m ":wrench: Patch ${VERSION}" --signoff
	git tag -a "v${VERSION}" -m "Patch ${VERSION}"


.PHONY: release
release: SHELL:=/bin/bash
release: all
	- rm -rf build/ dist/
	- git tag --delete "v${VERSION}"

	$(MAKE) changelog

	sed -i "s/__version__ = \(.*\)/__version__ = \"${VERSION}\"/g" argo/workflows/dsl/__about__.py

	python setup.py sdist bdist_wheel
	twine check dist/* || (echo "Twine check did not pass. Aborting."; exit 1)

	v=${VERSION}; git commit -a -m ":tada: Release $${v}" --signoff
	v=${VERSION}; git tag -a "v${VERSION}" -m "Release $${v}"


validate:
	@echo "Validating version '${VERSION}' on branch '{GIT_BRANCH}'"

	if [ "$(shell python -c \
		"from semantic_version import validate; print( validate('${VERSION}') )" \
	)" != "True" ]; then \
		echo "Invalid version. Aborting."; \
		exit 1; \
	fi

changelog:
	RELEASE_VERSION=${VERSION} ./scripts/generate_changelog.sh
