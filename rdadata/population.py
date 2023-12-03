"""
POPULATION-related helper functions
"""

from collections import defaultdict
from typing import Dict


def populations(data: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    """Return a dictionary of geoid -> population."""

    pop_by_geoid: Dict[str, int] = {k: v["TOTAL_POP"] for (k, v) in data.items()}
    return pop_by_geoid


def total_population(pop_by_geoid: Dict[str, int]) -> int:
    """Return the total population of the state."""

    total_pop: int = sum(pop_by_geoid.values())
    return total_pop


def calc_population_deviation(
    plan: list[dict[str, str | int]],
    pop_by_geoid: dict[str, int],
    total_pop: int,
    n_districts: int,
) -> float:
    """Calculate the population deviation of a map."""

    pop_by_district: defaultdict[int | str, int] = defaultdict(int)

    for p in plan:
        geoid: str = str(p["GEOID"])
        district: int = int(p["DISTRICT"])
        pop_by_district[district] += pop_by_geoid[geoid]

    max_pop: int = max(pop_by_district.values())
    min_pop: int = min(pop_by_district.values())
    target_pop: int = int(total_pop / n_districts)

    deviation: float = population_deviation_formula(max_pop, min_pop, target_pop)

    return deviation


def population_deviation_formula(max_pop: int, min_pop: int, target_pop: int) -> float:
    """The formula for population deviation.

    COPIED from rdapy, to simplify dependencies.
    """

    deviation: float = (max_pop - min_pop) / target_pop

    return deviation


### END ###
