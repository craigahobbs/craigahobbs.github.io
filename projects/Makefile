# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


MAKEJ ?= -j


.PHONY: clean commit help pull superclean report
help:
	@echo 'usage: make [clean|commit|gh-pages|gh-pages-check|pull|superclean]'
	@echo '            TYPE=[python|javascript|makefile|other]'


# Project rule header function - args are (project_name, type, rule)
define PROJECT_RULE_HEADER
.PHONY: _$(strip $(3))-$(strip $(1))
ifeq '$(TYPE)' ''
$(strip $(3)): _$(strip $(3))-$(strip $(1))
else ifeq '$(findstring $(strip $(2)),$(TYPE))' '$(strip $(2))'
$(strip $(3)): _$(strip $(3))-$(strip $(1))
endif
_$(strip $(3))-$(strip $(1)):
endef


# Project rules function - args are (project_name, type, git_repository)
define PROJECT_RULE
$(call PROJECT_RULE_HEADER, $(1), $(2), pull)
	if [ ! -d $$$$HOME/src/$(strip $(1)) ]; then git clone $(strip $(3)) $$$$HOME/src/$(strip $(1)); fi
	FAIL=$$$$(cd $$$$HOME/src/$(strip $(1)) && if [ "$$$$(git status -s)" != "" ]; then echo FAIL; fi); \
	if [ "$$$$FAIL" != "" ]; then \
		echo Error: Non-clean git status in $$$$HOME/src/$(strip $(1)); \
		exit 1; \
	fi
ifneq '$(strip $(2))' 'other'
	$(MAKE) -C $$$$HOME/src/$(strip $(1)) clean
endif
	cd $$$$HOME/src/$(strip $(1)) && git pull

$(call PROJECT_RULE_HEADER, $(1), $(2), commit)
ifeq '$(strip $(2))' 'makefile'
	$(MAKE) -C $$$$HOME/src/$(strip $(1)) commit
endif
ifeq '$(strip $(2))' 'python'
	$(MAKE) $(MAKEJ) -C $$$$HOME/src/$(strip $(1)) commit
endif
ifeq '$(strip $(2))' 'javascript'
	$(MAKE) $(MAKEJ) -C $$$$HOME/src/$(strip $(1)) commit
endif

$(call PROJECT_RULE_HEADER, $(1), $(2), gh-pages)
ifeq '$(strip $(2))' 'python'
	$(MAKE) $(MAKEJ) -C $$$$HOME/src/$(strip $(1)) gh-pages
endif
ifeq '$(strip $(2))' 'javascript'
	$(MAKE) $(MAKEJ) -C $$$$HOME/src/$(strip $(1)) gh-pages
endif

$(call PROJECT_RULE_HEADER, $(1), $(2), gh-pages-check)
ifneq '$(strip $(2))' 'makefile'
ifneq '$(strip $(2))' 'other'
	@if [ -d $$$$HOME/src/$(strip $(1)).gh-pages ]; then \
		FAIL=$$$$(cd $$$$HOME/src/$(strip $(1)).gh-pages && if [ "$$$$(git status -s)" != "" ]; then echo FAIL; fi); \
		if [ "$$$$FAIL" != "" ]; then \
			echo Error: Non-clean git status in $$$$HOME/src/$(strip $(1)).gh-pages; \
			exit 1; \
		else \
			rm -rf $$$$HOME/src/$(strip $(1)).gh-pages; \
		fi; \
	fi
endif
endif

$(call PROJECT_RULE_HEADER, $(1), $(2), clean)
ifneq '$(strip $(2))' 'other'
	$(MAKE) -C $$$$HOME/src/$(strip $(1)) clean
endif

$(call PROJECT_RULE_HEADER, $(1), $(2), superclean)
ifneq '$(strip $(2))' 'other'
	$(MAKE) -C $$$$HOME/src/$(strip $(1)) superclean
endif

report: _report-$(strip $(1))

.PHONY: _report-$(strip $(1))
_report-$(strip $(1)):
	@echo '$(strip $(1)) ($(strip $(2)))'
endef


# Project helper functions - args are (project_name, git_repository)
JAVASCRIPT_PROJECT = $(eval $(call PROJECT_RULE, $(1), javascript, $(2)))
PYTHON_PROJECT = $(eval $(call PROJECT_RULE, $(1), python, $(2)))
MAKEFILE_PROJECT = $(eval $(call PROJECT_RULE, $(1), makefile, $(2)))
OTHER_PROJECT = $(eval $(call PROJECT_RULE, $(1), other, $(2)))


# Javascript projects
$(call JAVASCRIPT_PROJECT, calc-script, 'git@github.com:craigahobbs/calc-script.git')
$(call JAVASCRIPT_PROJECT, chisel-doc, 'git@github.com:craigahobbs/chisel-doc.git')
$(call JAVASCRIPT_PROJECT, element-app, 'git@github.com:craigahobbs/element-app.git')
$(call JAVASCRIPT_PROJECT, element-model, 'git@github.com:craigahobbs/element-model.git')
$(call JAVASCRIPT_PROJECT, markdown-book-app, 'git@github.com:craigahobbs/markdown-book.git')
$(call JAVASCRIPT_PROJECT, markdown-charts, 'git@github.com:craigahobbs/markdown-charts.git')
$(call JAVASCRIPT_PROJECT, markdown-model, 'git@github.com:craigahobbs/markdown-model.git')
$(call JAVASCRIPT_PROJECT, markdown-up, 'git@github.com:craigahobbs/markdown-up.git')
$(call JAVASCRIPT_PROJECT, schema-markdown-doc, 'git@github.com:craigahobbs/schema-markdown-doc.git')
$(call JAVASCRIPT_PROJECT, schema-markdown-js, 'git@github.com:craigahobbs/schema-markdown-js.git')

# Python projects
$(call PYTHON_PROJECT, chisel, 'git@github.com:craigahobbs/chisel.git')
$(call PYTHON_PROJECT, markdown-up-py, 'git@github.com:craigahobbs/markdown-up-py.git')
$(call PYTHON_PROJECT, schema-markdown, 'git@github.com:craigahobbs/schema-markdown.git')
$(call PYTHON_PROJECT, simple-git-changelog, 'git@github.com:craigahobbs/simple-git-changelog.git')
$(call PYTHON_PROJECT, template-specialize, 'git@github.com:craigahobbs/template-specialize.git')
$(call PYTHON_PROJECT, unittest-parallel, 'git@github.com:craigahobbs/unittest-parallel.git')

# Makefile projects
$(call MAKEFILE_PROJECT, javascript-build, 'git@github.com:craigahobbs/javascript-build.git')
$(call MAKEFILE_PROJECT, javascript-template, 'git@github.com:craigahobbs/javascript-template.git')
$(call MAKEFILE_PROJECT, python-build, 'git@github.com:craigahobbs/python-build.git')
$(call MAKEFILE_PROJECT, python-template, 'git@github.com:craigahobbs/python-template.git')
$(call MAKEFILE_PROJECT, sunrise, 'git@github.com:craigahobbs/sunrise.git')

# Other projects
$(call OTHER_PROJECT, craigahobbs.github.io, 'git@github.com:craigahobbs/craigahobbs.github.io.git')
$(call OTHER_PROJECT, day-hikes, 'git@github.com:craigahobbs/day-hikes.git')
$(call OTHER_PROJECT, hobbs-family-cookbook, 'git@github.com:craigahobbs/hobbs-family-cookbook.git')
$(call OTHER_PROJECT, other-hobbs-family-cookbook, 'git@github.com:craigahobbs/other-hobbs-family-cookbook.git')
$(call OTHER_PROJECT, solar, 'git@github.com:craigahobbs/solar.git')
