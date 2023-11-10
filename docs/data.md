# Precinct Data

Census and election data by precinct are stored in the `data` directory by state in CSV files of the form `{xx}_2020_data.csv`, where `xx` is the state abbreviation.
They have the following columns:

```
GEOID
TOTAL_POP
TOTAL_VAP
WHITE_VAP
HISPANIC_VAP
BLACK_VAP
NATIVE_VAP
ASIAN_VAP
PACIFIC_VAP
MINORITY_VAP
TOT_VOTES
REP_VOTES
DEM_VOTES
OTH_VOTES
```

`TOTAL_POP` is the total population of the precinct.
The `*_VAP` fields are the voting age population demographics for the precinct.
The `*_VOTES` fields are the votes for the precinct in the 2016-2020 DRA [election composite](https://medium.com/dra-2020/election-composites-13d05ed07864).