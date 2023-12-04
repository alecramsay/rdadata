#!/usr/bin/env python3

"""
EXTRACT ELECTION DATA & NORMALIZE IT.

For example:

$ scripts/extract_elections.py -s NC

For documentation, type:

$ scripts/extract_elections.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from csv import DictReader
from typing import Any

from rdadata import (
    path_to_file,
    file_name,
    read_json,
    write_csv,
    FileSpec,
    data_dir,
    census_dir,
    temp_dir,
    cycle,
    election_fields,
    geoid_field,
)


def main() -> None:
    """Extract election data & normalize it."""

    args: Namespace = parse_args()

    xx: str = args.state

    verbose: bool = args.verbose

    ### READ CONFIG FILE ###

    config_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "config"], "_", "json"
    )
    config: Dict[str, Any] = read_json(config_path)

    suffix: str = config["election_suffix"]
    input_geoid: str = config["geoid"]
    elections: List[str] = config["elections"]

    if suffix != "":
        suffix = "-" + suffix

    tot_votes: str = election_fields[0]
    rep_votes: str = election_fields[1]
    dem_votes: str = election_fields[2]
    oth_votes: str = election_fields[3]

    ### READ THE ELECTIONS CSV & EXTRACT THE DATA ###

    election: List[Dict] = list()
    total_fields: List[str] = [f"Tot_{e}" for e in elections]
    rep_fields: List[str] = [f"R_{e}" for e in elections]
    dem_fields: List[str] = [f"D_{e}" for e in elections]

    input_path: str = path_to_file([census_dir, xx]) + file_name(
        [cycle, "election", xx + suffix], "_", "csv"
    )

    with open(FileSpec(input_path).abs_path, "r", encoding="utf-8-sig") as file:
        reader: DictReader[str] = DictReader(
            file, fieldnames=None, restkey=None, restval=None, dialect="excel"
        )

        for row_in in reader:
            row_out: Dict = dict()
            row_out[geoid_field] = row_in[input_geoid]
            row_out[tot_votes] = sum([int(row_in[x]) for x in total_fields])
            row_out[rep_votes] = sum([int(row_in[x]) for x in rep_fields])
            row_out[dem_votes] = sum([int(row_in[x]) for x in dem_fields])
            row_out[oth_votes] = (
                row_out[tot_votes] - row_out[rep_votes] - row_out[dem_votes]
            )

            election.append(row_out)

    ### WRITE THE NORMALIZED CENSUS DATA TO A CSV ###

    output_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "election"], "_", "csv"
    )
    write_csv(
        output_path,
        election,
        [geoid_field] + election_fields,
    )


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Extract election data from a vtd_data CSV file."
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
