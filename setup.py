from setuptools import setup, find_packages

"""
https://python-packaging.readthedocs.io/en/latest/minimal.html
https://packaging.python.org/en/latest/specifications/declaring-project-metadata/

Once:

$ python3 -m pip install --upgrade build
$ python3 -m pip install --upgrade twine

Each iteration:

$ python3 -m build
$ python3 -m twine upload --repository pypi dist/rdadata-x.y.z*.*

"""

setup(
    name="rdadata",
    version="1.2.0",
    description="Redistricting analytics data",
    url="https://github.com/dra2020/rdadata",
    author="alecramsay",
    author_email="a73cram5ay@gmail.com",
    license="MIT",
    packages=[
        "rdadata",
    ],
    install_requires=[
        "fiona",
        "geopandas",
        "libpysal",
        "pytest",
        "shapely",
    ],
    zip_safe=False,
)
