# pyright: basic

"""
UNION FIND

Copied from proebsting/dccvt.
Todd Proebsting wrote this code.
"""

from typing import Iterable, Set, List

from scipy.cluster.hierarchy import DisjointSet


class IntUnionFind:
    def __init__(self, vals: Iterable[int]):
        self._ds = DisjointSet(vals)

    def merge(self, a: int, b: int) -> None:
        self._ds.merge(a, b)

    def subsets(self) -> List[Set[int]]:
        return self._ds.subsets()

    def connected(self, a: int, b: int) -> bool:
        return self._ds.connected(a, b)

    @property
    def n_subsets(self) -> int:
        return self._ds.n_subsets

    def __len__(self) -> int:
        return len(self._ds)

    def __repr__(self) -> str:
        return f"IntUnionFind({self._ds})"

    def __str__(self) -> str:
        return f"IntUnionFind({self._ds})"

    def __getitem__(self, key: int) -> int:
        return self._ds[key]

    def __iter__(self) -> Iterable[int]:
        return iter(self._ds)


class StrUnionFind:
    def __init__(self, vals: Iterable[str]):
        self._ds = DisjointSet(vals)

    def add(self, val: str) -> None:
        self._ds.add(val)

    def merge(self, a: str, b: str) -> None:
        self._ds.merge(a, b)

    def subsets(self) -> List[Set[str]]:
        return self._ds.subsets()

    def connected(self, a: str, b: str) -> bool:
        return self._ds.connected(a, b)

    def subset(self, a: str) -> Set[str]:
        return self._ds.subset(a)

    @property
    def n_subsets(self) -> int:
        return self._ds.n_subsets

    def __len__(self) -> int:
        return len(self._ds)

    def __repr__(self) -> str:
        return f"StrUnionFind({self._ds})"

    def __str__(self) -> str:
        return f"StrUnionFind({self._ds})"

    def __getitem__(self, key: str) -> str:
        return self._ds[key]

    def __iter__(self) -> Iterable[str]:
        return iter(self._ds)
