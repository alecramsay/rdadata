#!/usr/bin/env python3
#

"""
EXTRACT A CONTIGUITY GRAPH FOR A STATE & GEOGRAPHIC UNIT.

For example:

$ scripts/extract_graph.py -s NC
$ scripts/extract_graph.py -s MI -w

$ scripts/extract_graph.py -s KS -w -z

$ scripts/extract_graph.py -s OR -w

$ scripts/extract_graph.py -s NY -w -a
$ scripts/extract_graph.py -s CA -w -a

For documentation, type:

$ scripts/extract_graph.py -h

TODO - Make this work again. Save to JSON instead of pickling.

"""

import argparse
from argparse import ArgumentParser, Namespace

from rdadata import *


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
        "-w", "--water", dest="water", action="store_true", help="Water-only precincts"
    )
    parser.add_argument(
        "-a", "--adds", dest="adds", action="store_true", help="Additional adjacencies"
    )
    parser.add_argument(
        "-z",
        "--unpopulated",
        dest="unpopulated",
        action="store_true",
        help="Unpopulated precincts",
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()

    return args


def main() -> None:
    """Extract an adjacency graph from a shapefile."""

    args: Namespace = parse_args()

    xx: str = args.state
    water: bool = args.water
    adds: bool = args.adds
    unpopulated: bool = args.unpopulated
    verbose: bool = args.verbose

    #

    unit = study_unit(xx)
    unit_label: str = "vtd20" if unit == "vtd" else unit

    #

    assert not water  # NOTE - Handle water-only precincts in the code.
    assert not unpopulated  # NOTE - Handle unpopulated precincts in the code code.

    #

    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    id: str = unit_id(unit)

    shp_dir: str = file_name(["tl_2020", fips, unit_label], "_")
    shp_path: str = path_to_file([shapes_dir, xx, shp_dir]) + file_name(
        ["tl_2020", fips, unit_label], "_", "shp"
    )

    # Read the shapefile & extract the graph

    graph: Graph = Graph(shp_path, id)

    # Add connections as needed to make the graph derived from shapes fully connected

    if adds:
        adds_path: str = path_to_file([data_dir, xx]) + file_name(
            [xx, cycle, unit, "contiguity_mods"], "_", "csv"
        )
        mods: list = read_mods(adds_path)
        # NOTE - Assume all mods are additions. Nothing else is supported yet.

        for mod in mods:
            graph.add_adjacency(mod[1], mod[2])

    # NOTE - Water-only precincts are handled in Todd's baseline code.
    # # Remove water-only precincts

    # water_precincts: list = list()
    # if water:
    #     water_path: str = path_to_file([data_dir, xx]) + file_name(
    #         [xx, cycle, unit, "water_only"], "_", "csv"
    #     )  # GEOID,ALAND,AWATER
    #     types: list = [str, int, int]
    #     water_precincts = [row["GEOID"] for row in read_csv(water_path, types)]

    #     for w in water_precincts:
    #         if w in graph.nodes():
    #             print(f"Removing water-only precinct {w}.")
    #             graph.remove(w)

    # NOTE - Unpopulated precincts are handled in Todd's baseline code.
    # # Bridge over unpopulated precincts

    # if unpopulated:
    #     unpopulated_path: str = path_to_file([data_dir, xx]) + file_name(
    #         [xx, cycle, "vtd", "unpopulated"], "_", "csv"
    #     )  # NOTE - Only works for vtds right now
    #     types: list = [str]
    #     unpopulated_precincts = [
    #         row["GEOID"] for row in read_csv(unpopulated_path, types)
    #     ]

    #     print("Bridging over unpopulated precincts.")
    #     for z in unpopulated_precincts:
    #         if z in graph.nodes():
    #             graph.bridge(z)

    # Make sure the graph is consistent & fully connected

    if not graph.is_consistent():
        print(f"WARNING: Graph is not consistent.")
    if not graph.is_connected():
        print(f"WARNING: Graph is not fully connected.")

    # Pickle the graph

    graph_path: str = path_to_file([temp_dir]) + file_name(
        [xx, cycle, unit, "graph"], "_", "pickle"
    )
    write_pickle(graph_path, graph.data())

    # Also save it as pairs in a CSV file, but ignore OUT_OF_STATE connections

    pairs_path: str = path_to_file(["data", xx]) + file_name(
        [xx, str(cycle), unit, "adjacencies"], "_", "csv"
    )
    abs_path: str = FileSpec(pairs_path).abs_path

    with open(abs_path, "w") as f:
        for one, two in graph.adjacencies():
            if one != "OUT_OF_STATE" and two != "OUT_OF_STATE":
                print(f"{one},{two}", file=f)

    pass


if __name__ == "__main__":
    main()

### END ###
