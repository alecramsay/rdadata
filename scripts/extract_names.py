#!/usr/bin/env python3

"""
EXTRACT FRIENDLY NAMES BY PRECINCT GEOID

For example:

$ scripts/extract_names.py -s NC > data/NC/NC_2020_names.txt

For documentation, type:

$ scripts/extract_names.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from rdadata import (
    path_to_file,
    file_name,
    STATE_FIPS,
    names_dir,
    study_unit,
    unit_id,
    FileSpec,
)


def main() -> None:
    """Create a mapping of GEOIDs to friendly names."""

    args: Namespace = parse_args()

    fips_map: Dict[str, str] = STATE_FIPS

    xx: str = args.state
    fips: str = fips_map[xx]

    verbose: bool = args.verbose

    state_dir: str = xx

    ### READ THE CENSUS FILE ###

    unit: str = study_unit(xx)

    rel_path: str = path_to_file([names_dir, state_dir]) + file_name(
        ["NAMES", f"ST{fips}", xx, unit.upper()], "_", "txt"
    )
    id: str = unit_id(unit)

    abs_path: str = FileSpec(rel_path).abs_path
    with open(abs_path, "r", encoding="utf-8-sig") as f:
        line: str = f.readline()  # skip header

        print()
        print(f"GEOID,NAME")
        while line:
            line = f.readline()
            if line == "":
                break
            fields: List[str] = line.split("|")
            geoid: str = "".join([fields[0], fields[1], fields[2]])
            name: str = fields[3]
            print(f"{geoid},{name}")


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Create a mapping of precinct GEOIDs to friendly names."
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
