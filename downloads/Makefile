# Licensed under the MIT License
# https://github.com/craigahobbs/sunrise/blob/main/LICENSE

.DEFAULT_GOAL := help


.PHONY: help
help:
	@echo "usage: make [data|help]"


.PHONY: data
data:
    # JavaScript packages
	$(call JAVASCRIPT_DATA, calc-script)
	$(call JAVASCRIPT_DATA, element-model)
	$(call JAVASCRIPT_DATA, markdown-model)
	$(call JAVASCRIPT_DATA, markdown-up)
	$(call JAVASCRIPT_DATA, schema-markdown-doc)
	$(call JAVASCRIPT_DATA, schema-markdown)

    # Python packages
	$(call PYTHON_DATA, chisel)
	$(call PYTHON_DATA, markdown-up)
	$(call PYTHON_DATA, schema-markdown)
	$(call PYTHON_DATA, simple-git-changelog)
	$(call PYTHON_DATA, template-specialize)
	$(call PYTHON_DATA, unittest-parallel)


JAVASCRIPT_DATA = curl -s "https://npm-stat.com/api/download-counts?package=$(strip $1)"`python -c "$$JAVASCRIPT_RANGE"` \
    > "data/javascript-$(strip $1).json"


PYTHON_DATA = curl -s "https://pypistats.org/api/packages/$(strip $1)/overall" \
    > "data/python-$(strip $1).json"


define JAVASCRIPT_RANGE
import datetime
today = datetime.date.today()
year_ago = today.replace(year=today.year - 1)
print(f"&from={year_ago.isoformat()}&until={today.isoformat()}")
endef
export JAVASCRIPT_RANGE
