#!/usr/bin/env python3
#

"""
Join the census & election data for a state.

For example:

$ scripts/join_data.py -s NC

For documentation, type:

$ scripts/join_data.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from rdadata import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Join the census & election data for a state and index it by GEOID."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Join the census & election data for a state and index it by GEOID."""

    args: Namespace = parse_args()

    xx: str = args.state

    verbose: bool = args.verbose

    ### READ THE CENSUS DATA ###

    census_path: str = path_to_file([wip_dir]) + file_name(
        [xx, cycle, "census"], "_", "csv"
    )
    census: list = read_csv(census_path, [str] + [int] * 9)

    ### READ THE ELECTION DATA ###

    election_path: str = path_to_file([wip_dir]) + file_name(
        [xx, cycle, "election"], "_", "csv"
    )
    election: list = read_csv(election_path, [str] + [int] * 4)

    ### JOIN THE CENSUS & ELECTION DATA BY GEOID ###

    data: dict[str, dict[str, int]] = dict()

    for row in census:
        geoid: str = row[geoid_field]
        data[geoid] = {k: row[k] for k in census_fields if k != geoid_field}

    for row in election:
        geoid: str = row[geoid_field]
        data[geoid].update({k: row[k] for k in election_fields if k != geoid_field})

    ### WRITE THE DATA BACK OUT AS A CSV ###

    joined: list[dict] = list()
    for geoid in data:
        row: dict = {"GEOID": geoid}
        row.update(data[geoid])
        joined.append(row)

    ### PICKLE THE DATA ###

    output_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "data"], "_", "csv"
    )
    write_csv(output_path, joined, joined[0].keys())


if __name__ == "__main__":
    main()

### END ###
