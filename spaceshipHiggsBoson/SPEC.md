# Spaceship Higgs-Boson

A simulation of a spaceship powered by a Higgs-Boson drive

## Specification

Create a novel theoretical spacecraft design that uses the Higgs Boson as part of its propulsion. Create a 3D rendering of such a spacecraft in orbit of Earth, and launching for Alpha Centauri.

## Implementation

Implement the application described above:

- First, read the bare-script skill, `.claude/skills/bare-script/SKILL.md`, and `CLAUDE.md`.
- Implement the application in `spaceshipHiggsBoson.bare` with the main function `spaceshipHiggsBosonMain()`, which
  `spaceshipHiggsBoson.md` calls. Escape user-provided text with `markdownEscape` before printing it as Markdown.
- Write unit tests in `test/testSpaceshipHiggsBoson.bare` using the skill's unittest.bare and unittestMock.bare
  patterns - a render test per page state, a test for each named handler, and a callback-binding test for
  each control - with 100% coverage.
- Run `make commit` and fix every test failure and lint warning until it passes.
- Do not run `make run` - it starts a web server that never returns. The user runs it after this session ends.
