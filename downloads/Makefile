# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE

.DEFAULT_GOAL := help


.PHONY: help
help:
	@echo "usage: make [data|help]"


# Download command function
WGET_CMD = if which wget; then wget -q -c -O - $(1) > $(2); else curl -f -s -o $(2) $(1); fi


# Python package download rule
define PYTHON_DATA_RULE
.PHONY: python-$(strip $1)
python-$(strip $1):
	@echo Downloading data/python-$(strip $1).json
	@WGET_OUTPUT=$$$$($(call WGET_CMD, \
		"https://pypistats.org/api/packages/$(strip $1)/overall", \
		data/python-$(strip $1).json))

.PHONY: data
data: python-$(strip $1)
endef


# Python package download rules
$(eval $(call PYTHON_DATA_RULE, bare-script))
$(eval $(call PYTHON_DATA_RULE, chisel))
$(eval $(call PYTHON_DATA_RULE, markdown-up))
$(eval $(call PYTHON_DATA_RULE, schema-markdown))
$(eval $(call PYTHON_DATA_RULE, simple-git-changelog))
$(eval $(call PYTHON_DATA_RULE, template-specialize))
$(eval $(call PYTHON_DATA_RULE, unittest-parallel))
