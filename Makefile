# Licensed under the MIT License
# https://github.com/craigahobbs/craigahobbs.github.io/blob/main/LICENSE


.PHONY: help
help:
	@echo 'usage: make [clean|commit|gh-pages|help|superclean]'


.PHONY: clean
clean:
	$(MAKE) -C color-ramp clean
	$(MAKE) -C downloads clean
	$(MAKE) -C fruit-fly-trap clean
	$(MAKE) -C life clean
	$(MAKE) -C money clean


.PHONY: commit
commit:
	$(MAKE) -C color-ramp commit
	$(MAKE) -C downloads commit
	$(MAKE) -C fruit-fly-trap commit
	$(MAKE) -C life commit
	$(MAKE) -C money commit


.PHONY: gh-pages
gh-pages:
	$(MAKE) -C downloads gh-pages


.PHONY: superclean
superclean:
	$(MAKE) -C color-ramp superclean
	$(MAKE) -C downloads superclean
	$(MAKE) -C fruit-fly-trap superclean
	$(MAKE) -C life superclean
	$(MAKE) -C money superclean
