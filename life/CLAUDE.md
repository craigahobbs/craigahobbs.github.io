# CLAUDE.md

Notes for coding agents working in this directory.

## Project overview

Conway's Game of Life is a [BareScript](https://craigahobbs.github.io/bare-script/) frontend application that runs in
[MarkdownUp](https://craigahobbs.github.io/markdown-up/). It is part of the craigahobbs.github.io GitHub Pages site -
`index.html` loads MarkdownUp, which fetches `life.md`, which includes `life.bare` and calls its main function,
`lifeMain()`.

`life.bare` is the whole application:

- **Arguments** - `lifeArguments` (via `args.bare`) are the URL hash arguments (`#var.vPlay=false`, ...). `lifeMain`
  limits them to valid ranges. Every menu action except the pause-menu buttons is a plain link that changes the URL.
- **State** - the Life object, `{width, height, cells, initial}`, is stored in session storage (`lifeLoad`/`lifeSave`)
  and validated (`lifeValidate` - the `lifeSession` schema and the cells length) on load. `cells` is a row-major array
  of 0/1; `initial` is the encoded starting state.
- **Animation** - when playing, `lifeSetTimeout` schedules `lifeTimeout`, which computes the next generation
  (`lifeNext`), detects cycles up to `depth` generations (starting a new random board when found), redraws below the
  `lifeReset` anchor (`documentSetReset`), and reschedules, subtracting the time spent. The cycle-detection
  generations are carried to the next call in the `lifeLookahead` global, reused only if the next call's life is the
  identical (`systemIs`), unchanged object the previous call returned - so each tick computes one new generation.
- **Menus** - `lifeMenuElements` builds the play, save, or pause menu. The pause menu's Step/Random/Reset/Width/Height
  buttons and the board's cell click (`drawOnClick`) call the `lifeClick*` handlers.
- **Encoding** - `lifeEncode`/`lifeDecode` convert a Life object to/from the `load` argument string - the
  base64-encoded (`base64.bare`), gzip-compressed (`gzip.bare`) JSON of its `width`, `height`, and `cells`. `lifeDecode`
  returns null for an invalid string, and `lifeMain` ignores an invalid `load` argument.

## Authoring BareScript code

Before writing, modifying, or reviewing BareScript code, read the bare-script skill. It is the reference for the
language, the built-in and include libraries, the MarkdownUp application pattern, and the unit-test and mocking pattern.

## Commands

The Makefile includes [python-build](https://github.com/craigahobbs/python-build#readme)'s `Makefile.tool`, downloaded
on first use (copied from `../../python-build` if that checkout exists), which builds a Python virtual environment in
`build/` with the `bare` CLI and MarkdownUp.

- `make commit` - run the unit tests and lint; the gate before committing
- `make test` - run the unit tests (`TEST=<name>` runs one test)
- `make lint` - lint every script standalone
- `make run` - view the application in a browser (for the user, not for a coding agent - it starts a server that
  never returns)
- `make clean` - remove the build directory and the downloaded python-build `Makefile.tool`

The parent directory's Makefile runs `commit` and `clean` for this project, too.

## Tests

The unit tests are in `test/testLife.bare`, with mocking, expected-value, and callback-binding helpers in
`test/testLifeHelpers.bare`. `test/runTests.bare` is the runner (`test/runTests.md` runs it in the browser).

- `testLifeMockAll()` replaces `unittestMockAll()` in every test. It also mocks (without recording) `windowWidth` and
  `windowHeight` (a 400x307 window - a 10x10 board has 20-pixel cells and a 211x211 drawing), `mathRandom` (alternating
  0.1, 0.9, ... - alive, dead, ... at the default `initRatio`), and `datetimeNow` (advancing 100 ms per call).
- `testLifeCells(width, height, points, initial)` builds a Life object from its alive `[x, y]` points (the `initial`
  default is `'test'`), `testLifeCellsEncoded(width, height, points)` builds one whose `initial` is its encoding, and
  `testLifePoints(life)` gets the points back. `testLifeEncoded` is the literal encoding of a 10x10 board with (1, 1)
  alive.
- `testLifeMenuRender`, `testLifeMenuPlay`, `testLifeMenuPause`, `testLifeMenuColor`, and `testLifeBoardRender` build
  the expected `elementModelRender` calls (`testLifeMenuRenderPlay` and `testLifeMenuRenderPause` are the default
  arguments' menus). Menu links are literal URLs - note that `argsURL` sorts the arguments and
  omits values equal to their defaults (the Play link is `#var=`).
- Tests that set URL argument globals (`systemGlobalSet('vPlay', false)`) set them back to `null` at the end, and
  tests that check the `lifeLookahead` cache set it back to `{}` (empty).

## Performance

The tick (`lifeTimeout`) is the hot path - at the fastest rate (30 Hz) it has 33 ms. A profile-guided optimization
pass (60 ticks of a random 50x50 board, output byte-identical to the original) took the JavaScript runtime (the
browser's) from 2853 ms to 282 ms, and the Python runtime from 455 ms to 166 ms:

- Carry the cycle-detection lookahead between ticks (`lifeLookahead`) - 7 `lifeNext` calls per tick to 1
- `lifeNext` slides a window of three column sums over dead-padded row slices - no per-cell bounds checks
- `lifeDraw` finds the alive cells with the native `arrayIndexOf` - about 10% faster on JavaScript, but about 30%
  slower on Python, whose `arrayIndexOf` compares element by element (the browser runtime wins)

Measured neutral (don't retry): drawing with `for alive, iCell in cells` instead of `arrayIndexOf`. What remains is
about two-thirds `lifeNext` (about 8 cheap statements per cell) and one-third `drawPathRect` per alive cell.

## Conventions

- The unit tests must pass with 100% coverage - `make test` fails otherwise.
- `make test` runs in debug mode. Every `failed with error` line in its output must be preceded by a `NOTICE:` line
  from the test that expects it.
- Each menu/page state has a render test asserting the full mock call log, each handler has a test, and each callback
  (the pause-menu buttons, the board's cell click, the resize and timeout handlers) has a binding test.
- Never rely on data row order or object key order.
