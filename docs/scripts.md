# Helper Scripts

These scripts let you convert the primary data into other formats required by specific applications.

## Pairs of Adjacent Precincts

To convert the node/neighbors graph JSON file into a CSV of pairs of adjacent precincts:

```bash
scripts/make_adjacent_pairs.py -s XX
```

where `XX` is a state abbreviation.

## Points

To combine precinct (x, y) locations with total population:

```bash
scripts/make_points_file.py -s XX
```

where `XX` is a state abbreviation.