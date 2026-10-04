# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

The "Package Downloads" dashboard for craigahobbs.github.io: a client-rendered
[MarkdownUp](https://github.com/craigahobbs/markdown-up) application showing PyPI and npm download stats for
the author's packages. It is a static site served by GitHub Pages; there is no server-side code.

## Commands

The Makefile downloads `Makefile.tool` and `pylintrc` from
[python-build](https://github.com/craigahobbs/python-build) on first run (copied from `../../python-build` if
that checkout exists) and creates a venv in `build/env` with `bare-script`, `coverage`, and `pylint`.

- `make test` — BareScript tests (`test/runTests.bare`) and Python tests (`test/test_downloads.py`); both
  require 100% coverage. `make test TEST=testName` runs one BareScript test.
- `make lint` — pylint and BareScript static analysis of the app and tests
- `make commit` — run before committing (test + lint)
- `make data` — run `downloads.py` to refresh `downloads.json` (hits the pypistats.org and npm APIs)
- `make clean` / `make superclean` — remove `build/` and the downloaded python-build files

The parent repo's Makefile (`../Makefile`) runs `commit`/`clean` across the subprojects (`color-ramp`,
`downloads`, `money`).

## Architecture

Data pipeline and front end are decoupled through a single JSON file:

- `downloads.py` — the data updater. `PACKAGES` lists the tracked packages (name + `Python`/`JavaScript`
  language). It fetches daily download counts (pypistats `without_mirrors` category for Python, npm
  range API for the trailing year for JavaScript), merges them into the existing `downloads.json` (fresh
  rows replace existing rows for the same date; today's partial day is excluded; rows older than
  `--years` (default 5) Jan 1 are pruned), and writes it sorted by Date/Language/Package.
- `downloads.json` — the dataset: a flat array of `{Package, Language, Date, Downloads}` rows (~1.6 MB;
  don't read it whole). It is updated nightly by `../.github/workflows/nightly-downloads.yml`, which runs
  `downloads.py` and commits as "downloads - update data" — that is what most git history consists of.
- `index.html` → loads MarkdownUp with `downloads.md`, whose `markdown-script` block includes
  `downloads.bare` and calls `downloadsMain` with options (e.g. the `featured` package map used to split
  the time chart into featured/non-featured).
- `downloads.bare` — the BareScript app. URL arguments (`downloadsArguments`, via `args.bare`) select the
  view: index table (monthly averages over trailing `days`), `page=chart` (monthly line charts for all
  packages), or a per-package dashboard when `name` and `language` are set. All views share
  `downloadsDataLoad` (fetches all of `downloads.json` and adds a `Unique` label that
  disambiguates packages published under the same name in both languages with ` (py)`/` (js)`).

Trailing averages use the window (maxDate - days, maxDate] — exactly `days` days — and are computed from
all loaded data *before* the `years` filter (`downloadsDataYears`), so averages don't depend on `years` and
the daily chart's average line starts at the first displayed date. The BareScript tests pin these boundaries
with a small fixture in `test/testDownloads.bare`; keep them passing when touching date math.

To add a tracked package, add it to `PACKAGES` in `downloads.py`; the front end picks it up from the data.
Use the `bare-script` skill when editing `downloads.bare`.
