# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


# Dependencies installed into the build virtual environment
TESTS_REQUIRE := bare-script

# Python virtual environment paths
VENV_DIR := build/venv
VENV_BIN := $(VENV_DIR)/bin
VENV_BUILD := $(VENV_DIR).build


.DEFAULT_GOAL := help


.PHONY: help
help:
	@echo "usage: make [clean|commit|lint|run|test]"


# Run the tests then lint - the pre-commit gate
.PHONY: commit
commit: test lint


# Run the unit tests (TEST="testName" runs one test); -d surfaces builtin debug logs
.PHONY: test
test: $(VENV_BUILD)
	$(VENV_BIN)/bare -d -m test/runTests.bare$(if $(TEST), -v vUnittestTest "'$(TEST)'")


# Statically analyze (and execute) every script, standalone
.PHONY: lint
lint: $(VENV_BUILD)
	$(VENV_BIN)/bare -x -m *.bare test/*.bare


# View the app in a browser (MarkdownUp local server)
.PHONY: run
run: $(VENV_BUILD)
	$(VENV_BIN)/pip install markdown-up
	$(VENV_BIN)/markdown-up colorRamp.md


# Remove the build directory (and the virtual environment)
.PHONY: clean
clean:
	rm -rf build/


# Build the virtual environment with the bare CLI, once
$(VENV_BUILD):
	mkdir -p $(VENV_DIR)
	python3 -m venv --upgrade-deps $(VENV_DIR)
	$(VENV_BIN)/pip install $(TESTS_REQUIRE)
	touch $@
