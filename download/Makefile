# Licensed under the MIT License
# https://github.com/craigahobbs/sunrise/blob/main/LICENSE

.DEFAULT_GOAL := help


.PHONY: help
help:
	@echo "usage: make [data|help]"


.PHONY: data
data:
	curl -s "https://pypistats.org/api/packages/chisel/overall" > "data/chisel.json"
	curl -s "https://pypistats.org/api/packages/markdown-up/overall" > "data/markdown-up.json"
	curl -s "https://pypistats.org/api/packages/schema-markdown/overall" > "data/schema-markdown.json"
	curl -s "https://pypistats.org/api/packages/simple-git-changelog/overall" > "data/simple-git-changelog.json"
	curl -s "https://pypistats.org/api/packages/template-specialize/overall" > "data/template-specialize.json"
	curl -s "https://pypistats.org/api/packages/unittest-parallel/overall" > "data/unittest-parallel.json"
