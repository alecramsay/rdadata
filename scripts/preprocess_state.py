#!/usr/bin/env python3

"""
PREPROCESS THE DATA & SHAPES FOR A STATE

For example:

$ scripts/preprocess_state.py -s NC
$ scripts/preprocess_state.py -s NY -a

For documentation, type:

$ scripts/preproces_state.py -h

NOTE - Before running this script for a state, you have to create a config file for it.

"""

import argparse
from argparse import ArgumentParser, Namespace

import os


def main() -> None:
    """Preprocess the data & shapes for a state."""

    args: Namespace = parse_args()

    xx: str = args.state
    adds: bool = args.adds

    verbose: bool = args.verbose

    #

    adds_flag: str = "-a" if adds else ""

    ### RUN THE SCRIPTS ###

    commands: List[str] = [
        "scripts/extract_census.py -s {xx}",
        "scripts/extract_elections.py -s {xx}",
        "scripts/join_data.py -s {xx}",
        "scripts/extract_shape_data.py -s {xx}",
        "scripts/extract_graph.py -s {xx} {adds_flag}",
        "scripts/extract_metadata.py -s {xx}",
    ]

    for command in commands:
        command = command.format(xx=xx, adds_flag=adds_flag)
        print(f"{command}")
        os.system(command)


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Preprocess the data & shapes for a state."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-a", "--adds", dest="adds", action="store_true", help="Additional adjacencies"
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


if __name__ == "__main__":
    main()

### END ###
