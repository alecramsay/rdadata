# Graph of Precincts

The graph JSON files are stored in the `data` directory by state in files of the form `{xx}_2020_graph.json`, where `xx` is the state abbreviation.

Both nodes and neighbors are precinct GEOIDs.
For example:

```json
    "37025008-00": [
        "37025005-00",
        "37025009-00",
        "37167000020",
        "37025007-00",
        "37167000019",
        "37025011-02",
        "37025006-00"
    ],
```

The graph includes the virtual "OUT_OF_STATE" node, which is adjacent to all precincts on the border of the state.

See the [helper scripts](./scripts.md) for how to convert the graph into pairs of adjacent precincts.