#!/usr/bin/env python3

"""
A HELPER SCRIPT TO CONVERT A GRAPH JSON TO AN ADJACENT PAIRS CSV

For example:

$ scripts/make_adjacent_pairs.py -s NC

For documentation, type:

$ scripts/make_adjacent_pairs.py -h

"""

import os

import argparse
from argparse import ArgumentParser, Namespace

from rdadata import path_to_file, file_name, read_json, FileSpec, data_dir, cycle, Graph


def main() -> None:
    """Convert a node/neighbors graph to pairs of adjacent precincts."""

    args: Namespace = parse_args()

    xx: str = args.state
    dest_dir: str = os.path.expanduser(args.output)

    verbose: bool = args.verbose

    ### READ THE GRAPH JSON ###

    graph_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "graph"], "_", "json"
    )
    graph_data: Dict = read_json(graph_path)

    ### CONVERT IT TO PAIRS OF ADJACENT PRECINCTS ###

    graph: Graph = Graph(graph_data)

    pairs_path: str = dest_dir + file_name([xx, cycle, "adjacencies"], "_", "csv")
    abs_path: str = FileSpec(pairs_path).abs_path

    with open(abs_path, "w") as f:
        for one, two in graph.adjacencies():
            if one != "OUT_OF_STATE" and two != "OUT_OF_STATE":
                print(f"{one},{two}", file=f)


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Convert a node/neighbors graph to pairs of adjacent precincts."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output",
        default="~/Downloads/",
        help="Path to output directory",
        type=str,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()

    return args


if __name__ == "__main__":
    main()

### END ###
