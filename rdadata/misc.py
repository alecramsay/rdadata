"""
MISCELLANEOUS helper functions
"""

from .constants import STATE_FIPS


def starting_seed(xx: str, N: int, K: int = 1) -> int:
    fips: str = STATE_FIPS[xx]
    start: int = K * N * int(fips)

    return start
