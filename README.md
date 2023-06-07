# Bowling Calculator

This app will calculate a bowling score frame-by-frame given a set of rolls.

## Initial Setup

There is one base system requirement: Python 3.10 or greater

With that installed, you can ensure your system has the `poetry` package manager
by calling `python install --upgrade poetry`.
(Note that if python3.10+ is not your default Python,
this command may vary and be `python3.10` or something similar, depending on
your specific situation)

Once Poetry is in place, you can set up all requirements by calling `poetry
install`, which will prepare all packages and make the CLI scripts accessible
for you.

## CLI Usage

You can calculate a score from the command line by calling `poetry run bowling`,
and providing the current set of rolls as arguments.

For example: `poetry run bowling 2 7 1 / X 5 2` will return `[9, 20, 17, 7]`

You may also pass in a `--pretty` flag before or after the rolls
to have the scores presented in a pretty-printed table in the console.

## API Usage

To start up the API, call `poetry run api`.

You can then browse the Swagger documentation at `http://localhost:8123/docs`,
or send API requests to `http://localhost:8123`.

For example:

    $ curl -X POST -H "Content-Type: application/json" localhost:8123 -d '["1", "2"]'
    > [3]

## Development

This codebase is written in Python,
using the `FastAPI` framework for the API,
and `rich` for CLI pretty-printing.

It is also style and format checked/corrected using `ruff`, `black`, and `mypy`.

As you edit the code,
you can check your style/formatting by running `poetry run lint`.

