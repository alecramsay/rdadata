#!/usr/bin/env python3

"""
RUN A BATCH OF COMMANDS

To run:

$ scripts/run_batch.py

"""

import os
from rdadata import ENSEMBLE_STATES

for xx in ENSEMBLE_STATES:
    if xx == "NC":
        continue

    command: str = f"scripts/extract_shape_data.py -s {xx}"
    command = command.format(xx=xx)
    print(command)
    os.system(command)


### END ###
