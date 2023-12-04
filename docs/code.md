# Shared Code

This shared code is in the `rdadata` package:

- **constants.py** - many recurring constants, e.g., state FIPS codes
- **readwrite.py** - utilities to read and write files - FileSpec, file_name, path_to_file, read_csv, write_csv, read_json,write_json, read_shapes, write_pickle, read_pickle, smart_open
- **approxequal.py** - utilities for determining approximate equality - approx_equal, dict_approx_equal
- **geoutils.py** - utilities for dealing with geoids - GeoID, study_unit, unit_id
- **graph.py** - utilities for dealing with adjacency graphs - Graph, is_connected, read_mods
- **population.py** - utilities for dealing with census populations - populations, total_population, calc_population_deviation
- **energy.py** - utilities for preparing to and the calculating energy of a plan - calc_energy, mkPoints, mkAdjacencies, index_geoids, index_data, index_points, index_assignments, LatLong, Point, Assignment,
- **requireargs** - a utility that adds a debug/explicit mode to scripts - require_args
- **timers.py** - Timer, time_function
- **misc.py** - starting_seed, for generating repeatable random numbers