# Licensed under the MIT License
# https://github.com/craigahobbs/sunrise/blob/main/LICENSE

.DEFAULT_GOAL := help


.PHONY: help
help:
	@echo "usage: make [data|help]"


.PHONY: data
data:
    # JavaScript packages
	curl -s "https://npm-stat.com/api/download-counts?package=calc-script"`python -c "$$NPM_RANGE"` > "data/javascript-calc-script.json"
	curl -s "https://npm-stat.com/api/download-counts?package=element-model"`python -c "$$NPM_RANGE"` > data/javascript-element-model.json
	curl -s "https://npm-stat.com/api/download-counts?package=markdown-model"`python -c "$$NPM_RANGE"` > data/javascript-markdown-model.json
	curl -s "https://npm-stat.com/api/download-counts?package=markdown-up"`python -c "$$NPM_RANGE"` > data/javascript-markdown-up.json
	curl -s "https://npm-stat.com/api/download-counts?package=schema-markdown-doc"`python -c "$$NPM_RANGE"` > data/javascript-schema-markdown-doc.json
	curl -s "https://npm-stat.com/api/download-counts?package=schema-markdown"`python -c "$$NPM_RANGE"` > data/javascript-schema-markdown.json

    # Python packages
	curl -s "https://pypistats.org/api/packages/chisel/overall" > "data/python-chisel.json"
	curl -s "https://pypistats.org/api/packages/markdown-up/overall" > "data/python-markdown-up.json"
	curl -s "https://pypistats.org/api/packages/schema-markdown/overall" > "data/python-schema-markdown.json"
	curl -s "https://pypistats.org/api/packages/simple-git-changelog/overall" > "data/python-simple-git-changelog.json"
	curl -s "https://pypistats.org/api/packages/template-specialize/overall" > "data/python-template-specialize.json"
	curl -s "https://pypistats.org/api/packages/unittest-parallel/overall" > "data/python-unittest-parallel.json"


define NPM_RANGE
import datetime
today = datetime.date.today()
year_ago = today.replace(year=today.year - 1)
print(f"&from={year_ago.isoformat()}&until={today.isoformat()}")
endef
export NPM_RANGE
