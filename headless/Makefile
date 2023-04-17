# Licensed under the MIT License
# https://github.com/craigahobbs/sunrise/blob/main/LICENSE

.DEFAULT_GOAL := help


# Download .eslintrc.cjs
define WGET
ifeq '$$(wildcard $(notdir $(1)))' ''
$$(info Downloading $(notdir $(1)))
_WGET := $$(shell $(call WGET_CMD, $(1)))
endif
endef
WGET_CMD = if which wget; then wget -q -c $(1); else curl -f -Os $(1); fi
$(eval $(call WGET, https://raw.githubusercontent.com/craigahobbs/javascript-build/main/.eslintrc.cjs))


# Node
NODE_IMAGE ?= node:current-slim
NODE_DOCKER := $(if $(NO_DOCKER),,docker run -i --rm -u `id -u`:`id -g` -v `pwd`:`pwd` -w `pwd` $(NODE_IMAGE))


.PHONY: help
help:
	@echo "usage: make [clean|commit|lint|superclean]"


.PHONY: clean
clean:
	rm -rf build package-lock.json .eslintrc.cjs


.PHONY: superclean
superclean: clean
ifeq '$(NO_DOCKER)' ''
	-docker rmi -f $(NODE_IMAGE)
endif


.PHONY: commit
commit: lint


.PHONY: lint
lint: build/npm.build
	$(NODE_DOCKER) npx --prefix ./build/ eslint -c .eslintrc.cjs -f unix .eslintrc.cjs$(if $(ESLINT_ARGS), $(ESLINT_ARGS))


build/npm.build:
ifeq '$(NO_DOCKER)' ''
	if [ "$$(docker images -q $(NODE_IMAGE))" = "" ]; then docker pull -q $(NODE_IMAGE); fi
endif
	mkdir -p $(dir $@)
	cd build && ln -s ../package.json .
	$(NODE_DOCKER) npm install --prefix ./build/
	touch $@
