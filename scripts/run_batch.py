#!/usr/bin/env python3

"""
RUN A BATCH OF COMMANDS

To run:

$ scripts/run_batch.py

"""

import os
from rdadata import *

for xx in ENSEMBLE_STATES:
    command: str = f"scripts/join_data.py -s {xx}"
    print(command)
    os.system(command)


### END ###
