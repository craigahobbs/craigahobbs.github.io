# Download python-build
PYTHON_BUILD_DIR ?= ../python-build
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


# The application
APP := spaceshipHiggsBoson


help:
	@echo "            [run]"


clean:
	rm -rf Makefile.tool


# The coding agent - Claude Code, Claude Code with an Ollama model (OLLAMA="model"), or Grok Build (GROK=1)
ifneq ($(GROK),)
AGENT := Grok Build
AGENT_CMD := grok --effort high
else ifneq ($(OLLAMA),)
AGENT := Claude Code with $(OLLAMA)
AGENT_CMD := ollama launch claude --model $(OLLAMA) --yes --
else
AGENT := Claude Code
AGENT_CMD := claude --model opus --effort high
endif


# Generate the application from its specification, if it doesn't exist. The coding agent runs interactively
# with file edits pre-approved - exit the session when it finishes
$(APP).bare: | $(DEFAULT_VENV_BUILD)
	@test -z "$$CLAUDECODE$$GROK_AGENT" || { echo "$@ does not exist - create it first (it is not generated inside a coding agent)"; exit 1; }
	@echo
	@echo "========================================================================"
	@echo "  Generating $@ from SPEC.md with $(AGENT)..."
	@echo "========================================================================"
	@echo
	$(AGENT_CMD) --permission-mode acceptEdits @SPEC.md
	test -f $@


# Run the unit tests (TEST="testName" runs one test); -d surfaces builtin debug logs
test: $(DEFAULT_VENV_BUILD) $(APP).bare
	$(DEFAULT_VENV_BIN)/bare -d -m test/runTests.bare$(if $(TEST), -v vUnittestTest "'$(TEST)'")


# Lint every script standalone. -x lints and executes (libraries + test files);
# -s lints the test runners without executing them (that's `make test`).
lint: $(DEFAULT_VENV_BUILD) $(APP).bare
	$(DEFAULT_VENV_BIN)/bare -x -m *.bare test/test*.bare
	$(DEFAULT_VENV_BIN)/bare -s -m test/runTests.bare


# View the application in a browser (MarkdownUp local server)
.PHONY: run
run: $(DEFAULT_VENV_BUILD) $(APP).bare
	$(DEFAULT_VENV_BIN)/markdown-up $(APP).md
