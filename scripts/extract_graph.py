#!/usr/bin/env python3

"""
EXTRACT A CONTIGUITY GRAPH FOR A STATE & GEOGRAPHIC UNIT.

For example:

$ scripts/extract_graph.py -s NC
$ scripts/extract_graph.py -s NY -a

For documentation, type:

$ scripts/extract_graph.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from rdadata import (
    path_to_file,
    file_name,
    read_json,
    write_json,
    data_dir,
    temp_dir,
    study_unit,
    unit_id,
    STATE_FIPS,
    shapes_dir,
    cycle,
    read_mods,
    Graph,
)


def main() -> None:
    """Extract an adjacency graph from a shapefile."""

    args: Namespace = parse_args()

    xx: str = args.state
    adds: bool = args.adds

    verbose: bool = args.verbose

    #

    unit = study_unit(xx)
    unit_label: str = "vtd20" if unit == "vtd" else unit

    fips_map: Dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    id: str = unit_id(unit)

    ### READ THE SHAPEFILE & EXTRACT THE GRAPH ###

    shp_dir: str = file_name(["tl_2020", fips, unit_label], "_")
    shp_path: str = path_to_file([shapes_dir, xx, shp_dir]) + file_name(
        ["tl_2020", fips, unit_label], "_", "shp"
    )
    graph: Graph = Graph(shp_path, id)

    ### ADD ADJACENCIES AS NEEDED FOR OPERATIONAL CONTIGUITY ###

    if adds:
        adds_path: str = path_to_file([data_dir, xx]) + file_name(
            [xx, cycle, unit, "contiguity_mods"], "_", "csv"
        )
        mods: List = read_mods(adds_path)
        # NOTE - Assume all mods are additions. Nothing else is supported yet.

        for mod in mods:
            graph.add_adjacency(mod[1], mod[2])

    ### MAKE SURE THE GRAPH IS CONSISTENT & FULLY CONNECTED ###

    if not graph.is_consistent():
        print(f"WARNING: Graph is not consistent.")
    if not graph.is_connected():
        print(f"WARNING: Graph is not fully connected.")

    ### WRITE THE GRAPH TO A JSON FILE ###

    graph_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "graph"], "_", "json"
    )
    write_json(graph_path, graph.data())


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Extract an adjacency graph from a shapefile."
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
