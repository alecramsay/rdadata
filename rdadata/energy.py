"""
ENERGY-related helper functions
"""

from collections import defaultdict
from typing import List, Dict, Tuple, Set, Any, NamedTuple

from .graph import Graph
from .union_find import StrUnionFind, IntUnionFind
from .constants import geoid_field


class LatLong(NamedTuple):
    lat: float
    long: float


class Point(NamedTuple):
    ll: LatLong
    pop: float


class Assignment(NamedTuple):
    site: int
    point: int
    pop: float


#


def mkPoints(
    data: Dict[str, Dict[str, int]],
    shapes: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Join precinct population with x,y location by GEOID."""

    points: List[Dict[str, Any]] = list()

    for geoid, values in data.items():
        point = dict()

        point[geoid_field] = geoid
        point["POP"] = values["TOTAL_POP"]
        point["X"] = shapes[geoid]["center"][0]
        point["Y"] = shapes[geoid]["center"][1]

        points.append(point)

    return points


def mkAdjacencies(graph: Graph) -> list[tuple[str, str]]:
    adjacencies: list[tuple[str, str]] = list()
    for one, two in graph.adjacencies():
        if one != "OUT_OF_STATE" and two != "OUT_OF_STATE":
            adjacencies.append((one, two))

    return adjacencies


#


def index_geoids(
    points: List[Dict[str, Any]],
) -> Dict[str, int]:
    """Index GEOIDs by offset."""

    offset_by_geoid: Dict[str, int] = {p[geoid_field]: i for i, p in enumerate(points)}
    return offset_by_geoid


def index_data(data: list[dict]) -> dict[str, dict[str, int]]:
    """Index precinct data by GEOID"""

    indexed: dict[str, dict[str, int]] = dict()
    for row in data:
        geoid: str = row[geoid_field]
        indexed[geoid] = row

    return indexed


#


def index_points(
    points: List[Dict[str, Any]],
    epsilon: float = 0.01,
) -> List[Point]:
    """Index points by GEOID offset."""

    ps: List[Point] = list()
    for p in points:
        ll: LatLong = LatLong(p["Y"], p["X"])
        pop: float = max(epsilon, p["POP"])
        ps.append(Point(ll, pop))

    assert epsilon > 0 or sum(p.pop for p in ps) == sum(p["POP"] for p in points)

    return ps


def index_pairs(
    offset_by_geoid: Dict[str, int],
    pairs: List[Tuple[str, str]],
) -> List[Tuple[int, int]]:
    """Index adjacent pairs by GEOID offset."""

    pairs = [
        (p1, p2) for p1, p2 in pairs if p1 != "OUT_OF_STATE" and p2 != "OUT_OF_STATE"
    ]
    adjacent_pairs: List[Tuple[int, int]] = [
        (offset_by_geoid[p1], offset_by_geoid[p2]) for p1, p2 in pairs
    ]

    geoids: Set[str] = set(offset_by_geoid.keys())
    report_disconnect(pairs, geoids, "all points")

    return adjacent_pairs


def index_assignments(
    assignments: List[Dict[str, str | int]],
    offset_by_geoid: Dict[str, int],
    pop_by_geoid: dict[str, int],
) -> List[Assignment]:
    """Index assignments by GEOID offset."""

    indexed_assignments: List[Assignment] = list()
    for p in assignments:
        geoid: str = str(p[geoid_field])
        district: int = int(p["DISTRICT"])  # NOTE - Assume 1-N districts for simplicity

        indexed: Assignment = Assignment(
            site=district - 1,
            point=offset_by_geoid[geoid],
            pop=float(pop_by_geoid[geoid]),
        )
        indexed_assignments.append(indexed)

    return indexed_assignments


def report_disconnect(pairs: List[Tuple[str, str]], geoids: Set[str], msg: str):
    ds = StrUnionFind(geoids)
    for p1, p2 in pairs:
        if (
            p1 != "OUT_OF_STATE"
            and p2 != "OUT_OF_STATE"
            and p1 in geoids
            and p2 in geoids
        ):
            ds.merge(p1, p2)
    if ds.n_subsets > 1:
        subset: Set[str] = min(ds.subsets(), key=len)
        if len(subset) > 10:
            summary = f"{list(subset)[:10]}..."
        else:
            summary = f"{list(subset)}"
        print(
            f"WARNING: {ds.n_subsets} disconnected {msg} regions, including: {summary}"
        )


#


def calc_energy(assignments: List[Assignment], points: List[Point]) -> float:
    """Calculate the energy of a map."""

    sites: List[LatLong] = get_centroids(assignments, points)
    total: float = sum(
        a.pop
        * squared_distance(
            sites[a.site], points[a.point].ll
        )  # not sqrt!!! moment of inertia!
        for a in assignments
    )

    return total


def squared_distance(a: LatLong, b: LatLong) -> float:
    return (a.lat - b.lat) * (a.lat - b.lat) + (a.long - b.long) * (a.long - b.long)


def get_centroids(assigns: List[Assignment], points: List[Point]) -> list[LatLong]:
    bysite: defaultdict[int, List[Assignment]] = defaultdict(list)
    for a in assigns:
        bysite[a.site].append(a)
    cs: List[LatLong] = []
    top: int = max(s for s in bysite.keys())
    for site in range(top + 1):
        persite: List[Assignment] = bysite[site]
        total: float = sum(a.pop for a in persite)
        lat: float = sum(points[a.point].ll.lat * a.pop for a in persite) / total
        long: float = sum(points[a.point].ll.long * a.pop for a in persite) / total
        cs.append(LatLong(lat, long))
    return cs


### END ###
