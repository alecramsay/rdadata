# Helper Functions

These functions let you convert the primary data into other formats required by specific applications.
To use them, TODO.

## Index Data by Precinct

To convert the CSV of census and election data into a dict indexed by precinct,
read the data CSV and call `index_data`:

```python
data: list[dict] = rdd.read_csv(data_path, [str] + [int] * 13)
indexed: dict[str, dict[str, int]] = index_data(data)
```
