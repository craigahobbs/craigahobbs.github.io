# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


.PHONY: help
help:
	@echo 'usage: make [clean|commit|gh-pages|help|superclean]'


.PHONY: clean
clean:
	$(MAKE) -C headless clean


.PHONY: commit
commit:
	$(MAKE) -C headless commit


.PHONY: gh-pages
gh-pages:
	$(MAKE) -C headless gh-pages


.PHONY: superclean
superclean:
	$(MAKE) -C headless superclean
