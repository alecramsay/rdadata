#!/usr/bin/env python3

"""
EXTRACT CENSUS DATA & NORMALIZE IT.

For example:

$ scripts/extract_census.py -s NC

For documentation, type:

$ scripts/extract_census.py -h

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
    census_fields,
    geoid_field,
)


def main() -> None:
    """Extract census data & normalize it."""

    args: Namespace = parse_args()

    xx: str = args.state

    verbose: bool = args.verbose

    ### READ CONFIG FILE ###

    config_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "config"], "_", "json"
    )
    config: Dict[str, Any] = read_json(config_path)

    suffix: str = config["census_suffix"]
    input_geoid: str = config["geoid"]
    total_field: str = config["total"]
    demo_fields: List[str] = config["demos"]

    if suffix != "":
        suffix = "-" + suffix

    total_pop: str = census_fields[0]
    total_vap: str = census_fields[1]
    white_vap: str = census_fields[2]
    minority_vap: str = census_fields[-1]

    ### READ THE CENSUS CSV & EXTRACT THE DATA ###

    census: List[Dict] = list()
    fields: List[str] = list(census_fields)
    fields.remove(total_pop)
    fields.remove(minority_vap)

    input_path: str = path_to_file([census_dir, xx]) + file_name(
        [cycle, "census", xx + suffix], "_", "csv"
    )

    with open(FileSpec(input_path).abs_path, "r", encoding="utf-8-sig") as file:
        reader: DictReader[str] = DictReader(
            file, fieldnames=None, restkey=None, restval=None, dialect="excel"
        )

        for row_in in reader:
            row_out: Dict = dict()
            row_out[geoid_field] = row_in[input_geoid]
            row_out[total_pop] = row_in[total_field]
            for i, field in enumerate(demo_fields):
                row_out[fields[i]] = row_in[demo_fields[i]]

            row_out[minority_vap] = int(row_out[total_vap]) - int(row_out[white_vap])

            census.append(row_out)

    ### WRITE THE NORMALIZED CENSUS DATA TO A CSV ###

    output_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, "census"], "_", "csv"
    )
    write_csv(output_path, census, [geoid_field] + census_fields)


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Extract census data from a vtd_data CSV file."
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
