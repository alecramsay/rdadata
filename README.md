# rdadata
Redistricting analytics data &amp; shared code

## Installation

To get the data locally, clone the repository:

```bash
$ git clone https://github.com/alecramsay/rdadata
$ cd rdadata
```

To use the shared code, install the package:

```bash
$ pip install rdadata
```

## Data

The data are stored in the `data` directory by state.
These pages describe each dataset:

- [Data](./docs/data.md): Census and election data by precinct.
- [Shapes](./docs/shapes.md): Shape properties by precinct.
- [Graph](./docs/graph.md): Precinct adjacency graph.

At present, data for [fifteen states](./docs/states.md) have been extracted.
In the future, we may extract data for other states.

## Code

Some shared code and scripts are described here:

- [Shared Code](./docs/code.md): Common code used in multiple applications.
- [Scripts](./docs/scripts.md): Scripts to re-format the data for specific applications.

## Sources

The data comes from the following sources:

-   The total census population & VAP demographics data comes from the 2020_census_XX-N.csv
    in the DRA [vtd_data](https://github.com/dra2020/vtd_data) GitHub repository, 
    where XX is the state abbreviation and N is the suffix.
    We take the latest version of the data, which is the one with the highest N.
-   The election data comes from the 2020_election_XX-N.csv in the same repo.
-   The shapes are copies of tl_2020_FF_vtd20.zip from [the Census Bureau](https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/VTD/2020/), 
    where FF is the state FIPS code, e.g., 37 for North Carolina.

Some things to be aware of:

-   If it exists, we use the adjusted population data instead of the official 2020 census total population data. 
-   For Florida, the official VTDs from the Census Bureau are bad. 
    We used DRA's corrected precinct shapes (GeoJSON), removed the intersections, and then converted it to a shapefile.
-   We simplify the precinct shapes (see `extract_shape_data.py`) to approximate the simplification that DRA does, so compactness measurements align.

## Testing

```bash
$ pytest
```
