# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


.PHONY: help
help:
	@echo 'usage: make [clean|commit|gh-pages|help|superclean]'


.PHONY: clean
clean:
	$(MAKE) -C downloads clean


.PHONY: commit
commit:
	$(MAKE) -C downloads commit


.PHONY: gh-pages
gh-pages:
	$(MAKE) -C downloads gh-pages


.PHONY: superclean
superclean:
	$(MAKE) -C downloads superclean
