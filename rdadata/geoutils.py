"""
GEO UTILITIES
"""

from functools import wraps


class GeoID:
    """Parse a 15-character GeoIDs into its component parts."""

    def __init__(self, id: str) -> None:
        self.state: str = id[0:2]
        self.county: str = id[0:5]  # id[2:5]
        self.tract: str = id[0:11]  # id[5:11]
        self.bg: str = id[0:12]  # id[11:12]
        self.block: str = id  # id[12:15]


def study_unit(state: str) -> str:
    if state in ["CA", "OR", "WV"]:
        return "bg"
    else:
        return "vtd"


def unit_id(units: str) -> str:
    if units in ["block", "state", "vtd"]:
        return "GEOID20"
    if units in ["bg", "tract"]:
        return "GEOID"
    raise ValueError(f"Invalid units: {units}")


### END ###
