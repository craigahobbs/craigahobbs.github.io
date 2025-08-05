# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


.PHONY: changed clean commit gh-pages gh-pages-check help list pull superclean
help:
	@echo 'usage: make [changed|clean|commit|gh-pages|gh-pages-check|help|list|markdown-up|pull|superclean]'
	@echo '            TYPE=[python|javascript|build|other]'


# Project rule header function - args are (project_type, project_name, rule)
define PROJECT_RULE_HEADER
.PHONY: _$(strip $(3))-$(strip $(2))
ifneq '$(findstring $(strip $(1)),$(if $(TYPE),$(TYPE),$(1)))' ''
$(strip $(3)): _$(strip $(3))-$(strip $(2))
endif
_$(strip $(3))-$(strip $(2)):
endef


# Project rules function - args are (project_type, project_name, git_repository, flags)
define PROJECT_RULES

# changed
$(call PROJECT_RULE_HEADER, $(1), $(2), changed)
	@if [ -d $$$$HOME/src/$(strip $(2)) ]; then \
		FAIL=$$$$(cd $$$$HOME/src/$(strip $(2)) && if [ "$$$$(git status -s)" != "" ]; then echo FAIL; fi); \
		if [ "$$$$FAIL" != "" ]; then \
			echo '$(strip $(2))'; \
		fi; \
	else \
		echo '$(strip $(2)) (missing)'; \
	fi


# clean
$(call PROJECT_RULE_HEADER, $(1), $(2), clean)
	@if [ -f $$$$HOME/src/$(strip $(2))/Makefile ]; then \
		$(MAKE) -C $$$$HOME/src/$(strip $(2)) clean; \
	fi


# commit
$(call PROJECT_RULE_HEADER, $(1), $(2), commit)
	@if [ -f $$$$HOME/src/$(strip $(2))/Makefile ]; then \
		$(MAKE)$(if $(findstring no-parallel, $(4)),, -j) -C $$$$HOME/src/$(strip $(2)) commit; \
	fi


# gh-pages
$(call PROJECT_RULE_HEADER, $(1), $(2), gh-pages)
	@if [ -f $$$$HOME/src/$(strip $(2))/Makefile ]; then \
		$(MAKE)$(if $(findstring no-parallel, $(4)),, -j) -C $$$$HOME/src/$(strip $(2)) gh-pages; \
	fi


# gh-pages-check
$(call PROJECT_RULE_HEADER, $(1), $(2), gh-pages-check)
	@if [ -d $$$$HOME/src/$(strip $(2)).gh-pages ]; then \
		if cd $$$$HOME/src/$(strip $(2)).gh-pages && [ -z "$$$$(git status --porcelain)" ] && git diff -w --exit-code > /dev/null; then \
			rm -rf $$$$HOME/src/$(strip $(2)).gh-pages; \
		else \
			echo '$(strip $(2)).gh-pages'; \
		fi; \
	fi


# list
$(call PROJECT_RULE_HEADER, $(1), $(2), list)
	@echo '$(strip $(2))'


# pull
$(call PROJECT_RULE_HEADER, $(1), $(2), pull)
	if [ ! -d $$$$HOME/src/$(strip $(2)) ]; then git clone $(strip $(3)) $$$$HOME/src/$(strip $(2)); fi
	@FAIL=$$$$(cd $$$$HOME/src/$(strip $(2)) && if [ "$$$$(git status -s)" != "" ]; then echo FAIL; fi); \
	if [ "$$$$FAIL" != "" ]; then \
		echo Error: Non-clean git status in $$$$HOME/src/$(strip $(2)); \
		exit 1; \
	fi
	cd $$$$HOME/src/$(strip $(2)) && git pull


# superclean
$(call PROJECT_RULE_HEADER, $(1), $(2), superclean)
	@if [ -f $$$$HOME/src/$(strip $(2))/Makefile ]; then \
		$(MAKE) -C $$$$HOME/src/$(strip $(2)) superclean; \
	fi


# markdown-up
ifneq '$(findstring markdown-up, $(4))' ''
$(call PROJECT_RULE_HEADER, $(1), $(2), markdown-up)
	$(MAKE) -C $$$$HOME/src/$(strip $(2)) markdown-up
endif

endef # PROJECT_RULES


# Javascript projects
$(eval $(call PROJECT_RULES, javascript, bare-script, 'git@github.com:craigahobbs/bare-script.git', markdown-up))
$(eval $(call PROJECT_RULES, javascript, element-model, 'git@github.com:craigahobbs/element-model.git'))
$(eval $(call PROJECT_RULES, javascript, markdown-model, 'git@github.com:craigahobbs/markdown-model.git'))
$(eval $(call PROJECT_RULES, javascript, markdown-up, 'git@github.com:craigahobbs/markdown-up.git'))
$(eval $(call PROJECT_RULES, javascript, schema-markdown-doc, 'git@github.com:craigahobbs/schema-markdown-doc.git'))
$(eval $(call PROJECT_RULES, javascript, schema-markdown-js, 'git@github.com:craigahobbs/schema-markdown-js.git'))

# Python projects
$(eval $(call PROJECT_RULES, python, bare-script-py, 'git@github.com:craigahobbs/bare-script-py.git', markdown-up))
$(eval $(call PROJECT_RULES, python, chisel, 'git@github.com:craigahobbs/chisel.git', markdown-up))
$(eval $(call PROJECT_RULES, python, markdown-up-py, 'git@github.com:craigahobbs/markdown-up-py.git'))
$(eval $(call PROJECT_RULES, python, ollama-chat, 'git@github.com:craigahobbs/ollama-chat.git'))
$(eval $(call PROJECT_RULES, python, schema-markdown, 'git@github.com:craigahobbs/schema-markdown.git'))
$(eval $(call PROJECT_RULES, python, simple-git-changelog, 'git@github.com:craigahobbs/simple-git-changelog.git'))
$(eval $(call PROJECT_RULES, python, template-specialize, 'git@github.com:craigahobbs/template-specialize.git'))
$(eval $(call PROJECT_RULES, python, unittest-parallel, 'git@github.com:craigahobbs/unittest-parallel.git'))

# Build projects
$(eval $(call PROJECT_RULES, build, javascript-build, 'git@github.com:craigahobbs/javascript-build.git', no-parallel))
$(eval $(call PROJECT_RULES, build, javascript-template, 'git@github.com:craigahobbs/javascript-template.git', no-parallel))
$(eval $(call PROJECT_RULES, build, python-build, 'git@github.com:craigahobbs/python-build.git', no-parallel))
$(eval $(call PROJECT_RULES, build, python-template, 'git@github.com:craigahobbs/python-template.git', no-parallel))

# Other projects
$(eval $(call PROJECT_RULES, other, craigahobbs.github.io, 'git@github.com:craigahobbs/craigahobbs.github.io.git'))
$(eval $(call PROJECT_RULES, other, day-hikes, 'git@github.com:craigahobbs/day-hikes.git'))
$(eval $(call PROJECT_RULES, other, hobbs-family-cookbook, 'git@github.com:craigahobbs/hobbs-family-cookbook.git'))
$(eval $(call PROJECT_RULES, other, npm-dependency-explorer, 'git@github.com:craigahobbs/npm-dependency-explorer.git'))
$(eval $(call PROJECT_RULES, other, other-hobbs-family-cookbook, 'git@github.com:craigahobbs/other-hobbs-family-cookbook.git'))
$(eval $(call PROJECT_RULES, other, solar, 'git@github.com:craigahobbs/solar.git'))
$(eval $(call PROJECT_RULES, other, sunrise, 'git@github.com:craigahobbs/sunrise.git'))
