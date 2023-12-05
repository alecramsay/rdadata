#!/usr/bin/env python3

"""
MAKE A POINTS FILE FOR INPUT TO THE ROOT/BASELINE CODE

For example:

$ scripts/make_points_file.py -s NC

For documentation, type:

$ scripts/make_points_file.py -h

"""

import os

import argparse
from argparse import ArgumentParser, Namespace

from typing import Dict, List

from rdadata import (
    path_to_file,
    file_name,
    read_csv,
    read_json,
    write_csv,
    FileSpec,
    data_dir,
    cycle,
    geoid_field,
)


def main() -> None:
    """Join the census & election data for a state and index it by GEOID."""

    args: Namespace = parse_args()

    xx: str = args.state
    dest_dir: str = os.path.expanduser(args.output)

    verbose: bool = args.verbose

    ### READ THE PRECINT DATA ###

    data_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "data"], "_", "csv"
    )
    data: List[Dict[str, str | int]] = read_csv(data_path, [str] + [int] * 13)

    ### READ THE SHAPES DATA ###

    shapes_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "shapes_simplified"], "_", "json"
    )
    shapes: Dict = read_json(shapes_path)

    ### JOIN THEM BY GEOID & SUBSET THE FIELDS ###

    points: List[Dict] = list()

    for row in data:
        point = dict()
        geoid: str = str(row[geoid_field])

        point["GEOID"] = geoid
        point["POP"] = row["TOTAL_POP"]
        point["X"] = shapes[geoid]["center"][0]
        point["Y"] = shapes[geoid]["center"][1]

        points.append(point)

    ### WRITE THE COMBINED DATA AS A CSV ###

    output_path: str = dest_dir + file_name([xx, cycle, "points"], "_", "csv")
    write_csv(output_path, points, ["GEOID", "POP", "X", "Y"], precision="{:.14f}")


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Make a points file for input to the root/baseline code."
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
