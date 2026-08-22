# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


# Download python-build
PYTHON_BUILD_DIR ?= ../../python-build
define WGET
ifeq '$$(wildcard $(notdir $(1)))' ''
$$(info Downloading $(notdir $(1)))
$$(shell [ -f $(PYTHON_BUILD_DIR)/$(notdir $(1)) ] && cp $(PYTHON_BUILD_DIR)/$(notdir $(1)) . || $(call WGET_CMD, $(1)))
endif
endef
WGET_CMD = if command -v wget >/dev/null 2>&1; then wget -q -c $(1); else curl -f -Os $(1); fi
$(eval $(call WGET, https://craigahobbs.github.io/python-build/Makefile.tool))


# Include python-build
include Makefile.tool


# Development dependencies
TESTS_REQUIRE := bare-script markdown-up


.PHONY: help
help:
	@echo "            [run]"


.PHONY: clean
clean:
	rm -rf Makefile.tool


# Run the unit tests (TEST="testName" runs one test); -d surfaces builtin debug logs
.PHONY: test
test: $(DEFAULT_VENV_BUILD)
	$(DEFAULT_VENV_BIN)/bare -d -m test/runTests.bare$(if $(TEST), -v vUnittestTest "'$(TEST)'")


# Lint every script standalone. -x lints and executes (libraries + test files);
# -s lints the test runners without executing them (that's `make test`).
.PHONY: lint
lint: $(DEFAULT_VENV_BUILD)
	$(DEFAULT_VENV_BIN)/bare -x -m *.bare test/test*.bare
	$(DEFAULT_VENV_BIN)/bare -s -m test/runTests.bare


# View the app in a browser (MarkdownUp local server)
.PHONY: run
run: $(DEFAULT_VENV_BUILD)
	$(DEFAULT_VENV_BIN)/markdown-up colorRamp.md
