#!/usr/bin/env python3

"""
JOIN THE CENSUS & ELECTION DATA FOR A STATE

For example:

$ scripts/join_data.py -s NC

For documentation, type:

$ scripts/join_data.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from typing import Dict, List

from rdadata import (
    path_to_file,
    file_name,
    read_csv,
    write_csv,
    data_dir,
    temp_dir,
    cycle,
    census_fields,
    geoid_field,
    election_fields,
)


def main() -> None:
    """Join the census & election data for a state and index it by GEOID."""

    args: Namespace = parse_args()

    xx: str = args.state

    verbose: bool = args.verbose

    ### READ THE CENSUS DATA ###

    census_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "census"], "_", "csv"
    )
    census: List[Dict[str, str | int]] = read_csv(census_path, [str] + [int] * 9)

    ### READ THE ELECTION DATA ###

    election_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "election"], "_", "csv"
    )
    election: List[Dict[str, str | int]] = read_csv(election_path, [str] + [int] * 4)

    ### JOIN THE CENSUS & ELECTION DATA BY GEOID ###

    data: Dict[str, Dict[str, int]] = dict()

    for row in census:
        geoid: str = row[geoid_field]
        data[geoid] = {k: row[k] for k in census_fields if k != geoid_field}

    for row in election:
        geoid: str = row[geoid_field]
        data[geoid].update({k: row[k] for k in election_fields if k != geoid_field})

    ### WRITE THE DATA BACK OUT AS A CSV ###

    joined: List[Dict] = list()
    for geoid in data:
        row: Dict = {"GEOID": geoid}
        row.update(data[geoid])
        joined.append(row)

    ### PICKLE THE DATA ###

    output_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "data"], "_", "csv"
    )
    write_csv(output_path, joined, joined[0].keys())


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


if __name__ == "__main__":
    main()

### END ###
