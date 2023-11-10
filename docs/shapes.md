# Precinct Shapes

Abstracted shape data by precinct are stored in the `data` directory by state in JSON files of the form `{xx}_2020_shapes_simplified.json`, where `xx` is the state abbreviation.
Each abstract has four properties:

- `center`: the (x, y) center of the precinct
- `area`: the area of the precinct
- `arcs`: a dictionary of the form `{neighbor_id: arc_length}` where `neighbor_id` is the ID of a neighboring precinct and `arc_length` is the length of the shared border between the two precincts
- `exterior`: a list of (x, y) points that define the exterior of the precinct

Here's an example:

```
    "37025008-00": {
        "center": [
            -80.43288599003887,
            35.402214400242414
        ],
        "area": 0.008036263500499881,
        "arcs": {
            "37025005-00": 0.01679623387150551,
            "37025009-00": 0.1312396193559532,
            "37167000020": 0.08408152079255174,
            "37025007-00": 0.03393812636263386,
            "37167000019": 0.073969981675411,
            "37025011-02": 0.014136168983005069,
            "37025006-00": 0.15573719660041122
        },
        "exterior": [
            [
                -80.396914,
                35.349689
            ],
            [
                -80.48795899999999,
                35.382571999999996
            ],
            [
                -80.48963499999999,
                35.383832
            ],
            [
                -80.510273,
                35.407679
            ],
            [
                -80.51218,
                35.41059
            ],
            [
                -80.513387,
                35.415873999999995
            ],
            [
                -80.510201,
                35.428317
            ],
            [
                -80.44020499999999,
                35.439989
            ],
            [
                -80.43882599999999,
                35.439973
            ],
            [
                -80.350754,
                35.419523
            ],
            [
                -80.396914,
                35.349689
            ]
        ]
    },
```

The `area`, `arcs`, and `exterior` points properties are used 
to infer district areas, perimeters, and diameters 
without having to actually create the district shapes.