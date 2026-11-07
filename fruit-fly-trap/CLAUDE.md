# CLAUDE.md

Notes for coding agents working in this directory.

## Project overview

The Fruit Fly Trap Maker is a [BareScript](https://craigahobbs.github.io/bare-script/) frontend application that runs
in [MarkdownUp](https://craigahobbs.github.io/markdown-up/). It is part of the craigahobbs.github.io GitHub Pages site -
`index.html` loads MarkdownUp, which fetches `fruit-fly-trap.md`, which includes `fruit-fly-trap.bare` and calls its
main function, `fruitFlyTrapMain()`.

`fruit-fly-trap.bare` is the whole application:

- **Arguments** - `fruitFlyTrapArguments` (via `args.bare`) are the URL hash arguments (`#var.vMetric=true`, ...). The
  measurement arguments (`diameter`, `height`, `offset`, `bottom`) have no argument defaults - `fruitFlyTrapMain`
  defaults them by units (imperial inches or metric centimeters). `print` is explicit, so links drop it.
- **Main page** - the introduction, the trap diagram (`fruitFlyTrapDiagram`), and the instructions. Every action is a
  plain link that changes the URL. Each measurement has Less/More links that step it by `delta`; a step that would make
  an invalid cone form (`fruitFlyTrapIsValidConeForm`) renders as plain text instead of a link. The cone height is
  `height - offset`, so the offset's Less checks the taller cone and its More the shorter one.
- **Print page** (`print`) - a Close link (hidden when printing) and the printable cone form (`fruitFlyTrapConeForm`),
  drawn at the physical size of the measurements (pixels per inch or centimeter).
- **Cone form** - the flattened cone is an annular sector plus a glue flap. `fruitFlyTrapConeForm` computes its inner
  and outer radii and angle, sizes the drawing to the sector's bounding box (one case per flap-angle quadrant), and
  draws the dashed cut line and the gray flap guide line.
- **Diagram** - `fruitFlyTrapDiagram` draws the glass, liquid, cone, and the h/o/d/b annotations, sized by
  `documentFontSize()`.

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

The unit tests are in `test/testFruitFlyTrap.bare`, with expected-value helpers in `test/testFruitFlyTrapHelpers.bare`.
`test/runTests.bare` is the runner (`test/runTests.md` runs it in the browser).

- Tests use plain `unittestMockAll()` - the app has no randomness or time, and it reads only `documentFontSize` (16)
  and `documentURL` (identity), whose mocks are not recorded.
- The expected drawings are literal element models: `testFruitFlyTrapDiagramRender()` is the diagram (the same for
  every argument), and `testFruitFlyTrapConeFormRender(width, height, formPath, guidePath)` is a cone form. The rect,
  path, and text helpers spell out draw.bare's attributes, nulls included. When the drawing code changes, dump the new
  call log with `jsonStringify(unittestMockEnd(), 4)` and update the literals - don't compute them with the app's
  functions.
- `testFruitFlyTrapIntro` and `testFruitFlyTrapInstructions(...)` build the main page's `markdownPrint` calls. Links
  are literal URLs - note that `argsURL` sorts the arguments and omits values equal to their defaults (the imperial
  Reset link is `#var=`).
- The `fruitFlyTrapConeForm` tests call it directly with pixel values chosen to land the flap angle in each quadrant.
- Tests that set URL argument globals (`systemGlobalSet('vMetric', true)`) set them back to `null` at the end.

## Conventions

- The unit tests must pass with 100% coverage - `make test` fails otherwise.
- `make test` runs in debug mode. Every `failed with error` line in its output must be preceded by a `NOTICE:` line
  from the test that expects it (there are none today).
- Each page state has a render test asserting the full mock call log. There are no callbacks - every control is a
  plain link, fully asserted by the render log. A new callback needs a binding test.
- Never rely on data row order or object key order.
