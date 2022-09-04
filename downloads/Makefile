# Licensed under the MIT License
# https://github.com/craigahobbs/sunrise/blob/main/LICENSE

.DEFAULT_GOAL := help


.PHONY: help
help:
	@echo "usage: make [data|help]"


# Download command function
WGET_CMD = if which wget; then wget -q -c -O $(2) $(1); else curl -f -s -o $(2) $(1); fi


# JavaScript package download rule
define JAVASCRIPT_DATA_RULE
.PHONY: javascript-$(strip $1)
javascript-$(strip $1):
	$(call WGET_CMD, \
		"https://npm-stat.com/api/download-counts?package=$(strip $1)"`python -c "$$$$JAVASCRIPT_RANGE"`, \
		data/javascript-$(strip $1).json)

.PHONY: data
data: javascript-$(strip $1)
endef


# Python script to compute JavaScript download URL range arguments
define JAVASCRIPT_RANGE
import datetime
today = datetime.date.today()
year_ago = today.replace(year=today.year - 1)
print(f"&from={year_ago.isoformat()}&until={today.isoformat()}")
endef
export JAVASCRIPT_RANGE


# Python package download rule
define PYTHON_DATA_RULE
.PHONY: python-$(strip $1)
python-$(strip $1):
	$(call WGET_CMD, \
		"https://pypistats.org/api/packages/$(strip $1)/overall", \
		data/python-$(strip $1).json)

.PHONY: data
data: python-$(strip $1)
endef


# JavaScript package download rules
$(eval $(call JAVASCRIPT_DATA_RULE, calc-script))
$(eval $(call JAVASCRIPT_DATA_RULE, element-model))
$(eval $(call JAVASCRIPT_DATA_RULE, markdown-model))
$(eval $(call JAVASCRIPT_DATA_RULE, markdown-up))
$(eval $(call JAVASCRIPT_DATA_RULE, schema-markdown-doc))
$(eval $(call JAVASCRIPT_DATA_RULE, schema-markdown))


# Python package download rules
$(eval $(call PYTHON_DATA_RULE, chisel))
$(eval $(call PYTHON_DATA_RULE, markdown-up))
$(eval $(call PYTHON_DATA_RULE, schema-markdown))
$(eval $(call PYTHON_DATA_RULE, simple-git-changelog))
$(eval $(call PYTHON_DATA_RULE, template-specialize))
$(eval $(call PYTHON_DATA_RULE, unittest-parallel))
