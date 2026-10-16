# CLAUDE.md

Notes for coding agents working in this repository.

## Project overview

Spaceship Higgs-Boson is a [BareScript](https://craigahobbs.github.io/bare-script/) frontend application that runs in
[MarkdownUp](https://craigahobbs.github.io/markdown-up/). A simulation of a spaceship powered by a Higgs-Boson drive

The application specification is `SPEC.md`. The application is `spaceshipHiggsBoson.bare`, whose main function
`spaceshipHiggsBosonMain()` is called from `spaceshipHiggsBoson.md`. It includes its parts:

- `spaceshipHiggsBosonCinema.bare` - the cinematography library - a cinema model (Schema Markdown) of films, scenes,
  shots, camera moves, actor blocking and beats, dialogue, titles, and sound cues, and its executor
- `spaceshipHiggsBosonFilm.bare` - the film of the voyage, in the cinema model, and its sets and cast
- `spaceshipHiggsBosonStoryboard.bare` - the storyboard page - the film, shot by shot
- `spaceshipHiggsBosonCast.bare` - the cast page - the film's actors, voices, and locations
- `spaceshipHiggsBosonModels.bare` - the detail levels, meshes, and scene objects
- `spaceshipHiggsBosonRender.bare` - the 3D renderer
- `spaceshipHiggsBosonPhysics.bare` - the mission and drive physics
- `spaceshipHiggsBosonAbout.bare` - the about page

Each part's unit tests are in its `test/test<Part>.bare` file (for example, `test/testSpaceshipHiggsBosonCinema.bare`),
with shared helpers in `test/testSpaceshipHiggsBosonHelpers.bare`.
The Makefile includes [python-build](https://github.com/craigahobbs/python-build#readme)'s `Makefile.tool`,
downloaded on first use, which builds a Python virtual environment with the `bare` CLI and MarkdownUp.

The project is publishable as-is on GitHub Pages: `index.html` loads MarkdownUp, which fetches `spaceshipHiggsBoson.md`,
and the empty `.nojekyll` file keeps GitHub Pages from processing the Markdown and `.bare` files with Jekyll.

## Authoring BareScript code

Before writing, modifying, or reviewing BareScript code, read the bare-script skill,
`.claude/skills/bare-script/SKILL.md`. It is the reference for the language, the built-in and include
libraries, the MarkdownUp application pattern, and the unit-test and mocking pattern.

## Commands

- `make commit` - run the unit tests and lint; the gate before committing
- `make test` - run the unit tests (`TEST=<name>` runs one test)
- `make lint` - lint every script standalone
- `make run` - view the application in a browser (for the user, not for a coding agent - it starts a server that
  never returns)
- `make clean` - remove the build directory and the downloaded python-build `Makefile.tool`

`make commit`, `make test`, and `make lint` depend on `spaceshipHiggsBoson.bare`, which the Makefile otherwise generates with
Claude Code - create `spaceshipHiggsBoson.bare` before running them.

## Conventions

- The unit tests must pass with 100% coverage - `make test` fails otherwise.
- Each page state has a render test, each named handler has a test, and each control's callback binding is tested.
- Escape user-provided text with `markdownEscape` before printing it as Markdown.
