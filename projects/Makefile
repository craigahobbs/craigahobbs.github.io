# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


MAKEJ ?= -j


.PHONY: changed clean commit help pull report superclean
help:
	@echo 'usage: make [changed|clean|commit|gh-pages|gh-pages-check|pull|report|superclean]'
	@echo '            TYPE=[python|javascript|makefile|other]'


# Project rule header function - args are (project_type, project_name, rule)
define PROJECT_RULE_HEADER
.PHONY: _$(strip $(3))-$(strip $(2))
ifneq '$(findstring $(strip $(1)),$(if $(TYPE),$(TYPE),$(1)))' ''
$(strip $(3)): _$(strip $(3))-$(strip $(2))
endif
_$(strip $(3))-$(strip $(2)):
endef


# Project rules function - args are (project_type, project_name, git_repository)
define PROJECT_RULES

# changed
$(call PROJECT_RULE_HEADER, $(1), $(2), changed)
	@FAIL=$$$$(cd $$$$HOME/src/$(strip $(2)) && if [ "$$$$(git status -s)" != "" ]; then echo FAIL; fi); \
	if [ "$$$$FAIL" != "" ]; then \
		echo '$(strip $(2))'; \
	fi


# clean
$(call PROJECT_RULE_HEADER, $(1), $(2), clean)
ifneq '$(strip $(1))' 'other'
	$(MAKE) -C $$$$HOME/src/$(strip $(2)) clean
endif


# commit
$(call PROJECT_RULE_HEADER, $(1), $(2), commit)
ifeq '$(strip $(1))' 'makefile'
	$(MAKE) -C $$$$HOME/src/$(strip $(2)) commit
endif
ifneq '$(strip $(1))' 'makefile'
ifneq '$(strip $(1))' 'other'
	$(MAKE) $(MAKEJ) -C $$$$HOME/src/$(strip $(2)) commit
endif
endif


# gh-pages
$(call PROJECT_RULE_HEADER, $(1), $(2), gh-pages)
ifneq '$(strip $(1))' 'makefile'
ifneq '$(strip $(1))' 'other'
	$(MAKE) $(MAKEJ) -C $$$$HOME/src/$(strip $(2)) gh-pages
endif
endif


# gh-pages-check
$(call PROJECT_RULE_HEADER, $(1), $(2), gh-pages-check)
ifneq '$(strip $(1))' 'makefile'
ifneq '$(strip $(1))' 'other'
	@if [ -d $$$$HOME/src/$(strip $(2)).gh-pages ]; then \
		FAIL=$$$$(cd $$$$HOME/src/$(strip $(2)).gh-pages && if [ "$$$$(git status -s)" != "" ]; then echo FAIL; fi); \
		if [ "$$$$FAIL" != "" ]; then \
			echo '$(strip $(2)).gh-pages'; \
		else \
			rm -rf $$$$HOME/src/$(strip $(2)).gh-pages; \
		fi; \
	fi
endif
endif


# pull
$(call PROJECT_RULE_HEADER, $(1), $(2), pull)
	if [ ! -d $$$$HOME/src/$(strip $(2)) ]; then git clone $(strip $(3)) $$$$HOME/src/$(strip $(2)); fi
	@FAIL=$$$$(cd $$$$HOME/src/$(strip $(2)) && if [ "$$$$(git status -s)" != "" ]; then echo FAIL; fi); \
	if [ "$$$$FAIL" != "" ]; then \
		echo Error: Non-clean git status in $$$$HOME/src/$(strip $(2)); \
		exit 1; \
	fi
ifneq '$(strip $(1))' 'other'
	$(MAKE) -C $$$$HOME/src/$(strip $(2)) clean
endif
	cd $$$$HOME/src/$(strip $(2)) && git pull


# report
$(call PROJECT_RULE_HEADER, $(1), $(2), report)
	@echo '$(strip $(2)) ($(strip $(1)))'


# superclean
$(call PROJECT_RULE_HEADER, $(1), $(2), superclean)
ifneq '$(strip $(1))' 'other'
	$(MAKE) -C $$$$HOME/src/$(strip $(2)) superclean
endif

endef # PROJECT_RULES


# Javascript projects
$(eval $(call PROJECT_RULES, javascript, calc-script, 'git@github.com:craigahobbs/calc-script.git'))
$(eval $(call PROJECT_RULES, javascript, element-app, 'git@github.com:craigahobbs/element-app.git'))
$(eval $(call PROJECT_RULES, javascript, element-model, 'git@github.com:craigahobbs/element-model.git'))
$(eval $(call PROJECT_RULES, javascript, markdown-book-app, 'git@github.com:craigahobbs/markdown-book.git'))
$(eval $(call PROJECT_RULES, javascript, markdown-model, 'git@github.com:craigahobbs/markdown-model.git'))
$(eval $(call PROJECT_RULES, javascript, markdown-up, 'git@github.com:craigahobbs/markdown-up.git'))
$(eval $(call PROJECT_RULES, javascript, schema-markdown-doc, 'git@github.com:craigahobbs/schema-markdown-doc.git'))
$(eval $(call PROJECT_RULES, javascript, schema-markdown-js, 'git@github.com:craigahobbs/schema-markdown-js.git'))

# Python projects
$(eval $(call PROJECT_RULES, python, chisel, 'git@github.com:craigahobbs/chisel.git'))
$(eval $(call PROJECT_RULES, python, markdown-up-py, 'git@github.com:craigahobbs/markdown-up-py.git'))
$(eval $(call PROJECT_RULES, python, schema-markdown, 'git@github.com:craigahobbs/schema-markdown.git'))
$(eval $(call PROJECT_RULES, python, simple-git-changelog, 'git@github.com:craigahobbs/simple-git-changelog.git'))
$(eval $(call PROJECT_RULES, python, template-specialize, 'git@github.com:craigahobbs/template-specialize.git'))
$(eval $(call PROJECT_RULES, python, unittest-parallel, 'git@github.com:craigahobbs/unittest-parallel.git'))

# Makefile projects
$(eval $(call PROJECT_RULES, makefile, javascript-build, 'git@github.com:craigahobbs/javascript-build.git'))
$(eval $(call PROJECT_RULES, makefile, javascript-template, 'git@github.com:craigahobbs/javascript-template.git'))
$(eval $(call PROJECT_RULES, makefile, python-build, 'git@github.com:craigahobbs/python-build.git'))
$(eval $(call PROJECT_RULES, makefile, python-template, 'git@github.com:craigahobbs/python-template.git'))
$(eval $(call PROJECT_RULES, makefile, sunrise, 'git@github.com:craigahobbs/sunrise.git'))

# Other projects
$(eval $(call PROJECT_RULES, other, craigahobbs.github.io, 'git@github.com:craigahobbs/craigahobbs.github.io.git'))
$(eval $(call PROJECT_RULES, other, day-hikes, 'git@github.com:craigahobbs/day-hikes.git'))
$(eval $(call PROJECT_RULES, other, hobbs-family-cookbook, 'git@github.com:craigahobbs/hobbs-family-cookbook.git'))
$(eval $(call PROJECT_RULES, other, other-hobbs-family-cookbook, 'git@github.com:craigahobbs/other-hobbs-family-cookbook.git'))
$(eval $(call PROJECT_RULES, other, solar, 'git@github.com:craigahobbs/solar.git'))
