https://packaging.python.org/en/latest/tutorials/packaging-projects/

Once:

$ python3 -m pip install --upgrade build
$ python3 -m pip install --upgrade twine

Each iteration:

* Update the version in pyproject.toml & setup.py. 
* Then:

$ python3 -m build
$ python3 -m twine upload --repository pypi dist/*

For a specific version, w/o deleting the others locally:

$ python3 -m twine upload --repository pypi dist/rdadata-x.y.z*.*

where x.y.z is the version number, e.g.:

$ python3 -m twine upload --repository pypi dist/rdadata-1.2.3*.*