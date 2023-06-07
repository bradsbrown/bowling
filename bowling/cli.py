import argparse

import rich
import rich.table
import sh

import bowling.calculator


def cli():
    parser = argparse.ArgumentParser("bowling")
    parser.add_argument("rolls", nargs="+")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    res = bowling.calculator.get_scores(args.rolls)
    if args.pretty:
        headers = [f"Frame {i + 1}" for i in range(len(res))]
        table = rich.table.Table(*headers, title="Bowling Scores")
        table.add_row(*[str(x) for x in res])
        rich.print(table)
    else:
        print(res)


def lint():
    sh.black(".")
    sh.ruff("--fix", ".")
    sh.mypy(".")
    sh.ls("newp")
