#!/usr/bin/env python3

"""
ABSTRACT PRECINCT SHAPES 
so the area, perimeter, and diameter of district shapes can be computed *implicitly*.

For example:

$ scripts/extract_shape_data.py -s NC

For documentation, type:

$ scripts/extract_shape_data.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from typing import Any, List, Dict, Tuple, Optional
from shapely.geometry import Polygon, MultiPolygon, Point

from rdadata import (
    path_to_file,
    file_name,
    read_json,
    write_json,
    read_shapes,
    STATE_FIPS,
    data_dir,
    shapes_dir,
    cycle,
    OUT_OF_STATE,
)


def find_center(shp) -> Tuple[float, float]:
    """Get a centroid-like point guaranteed to be w/in the feature"""

    x: float = shp.centroid.x
    y: float = shp.centroid.y

    if not shp.contains(Point(x, y)):
        pt: Point = shp.representative_point()
        x: float = pt.x
        y: float = pt.y

    return x, y


def main() -> None:
    """Abstract the precinct shapes for a state."""

    args: Namespace = parse_args()

    xx: str = args.state
    simplify: bool = not args.unsimplified

    verbose: bool = args.verbose

    #

    EPSILON: float = 1.0e-12  # NOTE - This overrides the constants.py value
    THRESHOLD: float = 0.000255  # more or less matches DRA simplification
    # THRESHOLD: float = 0.00026 # too high
    # THRESHOLD: float = 0.00025  # too low

    fips_map: Dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    ### LOAD THE GRAPH ###

    graph_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "graph"], "_", "json"
    )

    graph: Dict[str, List[str]] = read_json(graph_path)

    ### LOAD THE SHAPES ###

    geoid_field: str = "GEOID20"
    vtd_path: str = path_to_file([shapes_dir, xx]) + file_name(
        ["tl_2020", fips, "vtd20"], "_"
    )

    if xx == "FL":  # Use DRA's corrected precincts for Florida
        vtd_path = path_to_file([shapes_dir, xx]) + "tabblock.vtd.cleaned"
        geoid_field = "id"

    vtd_shps: dict
    other: Optional[Dict[str, Any]]
    vtd_shps, other = read_shapes(vtd_path, geoid_field)

    ### ABSTRACT THE SHAPES ###

    vtd_abstracts: Dict[str, Dict[str, Any]] = dict()

    for item in vtd_shps.items():
        geoid: str = item[0]
        shp: Polygon | MultiPolygon = item[1]

        if simplify:
            shp = shp.simplify(THRESHOLD, preserve_topology=True)

        center: Tuple[float, float] = find_center(shp)

        area: float = shp.area

        arcs: Dict[str, float] = dict()  # The shared border lengths by neighbor
        neighbors: List[str] = graph[geoid]
        perimeter: float = shp.length
        total_shared_border: float = 0.0

        for neighbor in neighbors:
            if neighbor == OUT_OF_STATE:
                continue
            if neighbor not in vtd_shps:
                print(f"WARNING: {neighbor} not in vtd_shps!")
                continue
            neighbor_shp: Polygon | MultiPolygon = vtd_shps[neighbor]
            shared_edge = shp.intersection(neighbor_shp)
            shared_border: float = shared_edge.length

            arcs[neighbor] = shared_border
            total_shared_border += shared_border

        remaining: float = perimeter - total_shared_border
        if remaining > EPSILON:
            arcs[OUT_OF_STATE] = remaining

        ch = shp.convex_hull
        pts: List[Tuple[float, float]] = list(ch.exterior.coords)

        vtd_abstracts[geoid] = {
            "center": center,
            "area": area,
            "arcs": arcs,
            "exterior": pts,
        }

    ### WRITE THE SHAPE DATA TO A JSON FILE ###

    shapes_name: str = (
        f"{xx}_{cycle}_shapes_simplified.json"
        if simplify
        else f"{xx}_{cycle}_shapes.json"
    )
    output_path: str = path_to_file([data_dir, xx]) + shapes_name
    write_json(output_path, vtd_abstracts)


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Copy the shapes for a state."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-u",
        "--unsimplified",
        dest="unsimplified",
        action="store_true",
        help="Simplify mode",
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


if __name__ == "__main__":
    main()

### END ###
