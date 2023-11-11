#!/usr/bin/env python3

"""
APPLICATION HELPERS
"""

from .constants import *


def index_data(data: list[dict]) -> dict[str, dict[str, int]]:
    """Index precinct data by GEOID"""

    indexed: dict[str, dict[str, int]] = dict()
    for row in data:
        geoid: str = row[geoid_field]
        indexed[geoid] = row

    return indexed


### END ###
