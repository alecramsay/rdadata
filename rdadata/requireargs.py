"""
REQUIRE ARGS - DEBUG & EXPLICIT MODES
"""

import sys
import argparse
from typing import Any, List, Dict, Optional


def require_args(
    args: argparse.Namespace, debug_mode: bool, debug_defaults: Dict[str, Any]
) -> argparse.Namespace:
    """This extends parser.parse_args() to enable two modes of operation:
    - debug: default values are used for the args in debug_defaults, regardless of user input or add_argument defaults
    - explicit: values are required for the args in debug_defaults, whether from user input or add_argument defaults
    """

    if debug_mode:
        for k, v in debug_defaults.items():
            setattr(args, k, v)
    else:  # explicit mode
        missing_args: List = list()
        for k, v in debug_defaults.items():
            if getattr(args, k) is None:
                missing_args.append(k)
        if missing_args:
            path_name: Optional[str] = sys.modules["__main__"].__file__
            module_name: str = (
                path_name.split("/")[-1] if path_name is not None else "unknown"
            )
            missing: str = "--" + ", --".join(missing_args)
            print(
                f"{module_name}: error: the following arguments are required: {missing}"
            )
            sys.exit()

    return args


def parse_args():
    """
    Examples:

    $ ./requireargs.py                                                                 # debug defaults
    $ ./requireargs.py --explicit                                                      # fails
    $ ./requireargs.py --explicit --requiredstr foo --requiredint 42                   # works
    $ ./requireargs.py --explicit --requiredstr foo --requiredint 42 --optionalint 100 # works

    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--requiredstr",
        type=str,
        help="A required string",
    )
    parser.add_argument("--requiredint", type=int, help="A required int")
    parser.add_argument("--optionalint", type=int, default=1000, help="An optional int")
    parser.add_argument(
        "--optionalfloat",
        type=float,
        default=0.02,
        help="An optional float",
    )
    parser.add_argument(
        "--optionalflag",
        dest="optionalflag",
        action="store_true",
        help="An optional flag",
    )

    # Include this pair of arguments to enable debug/explicit mode
    parser.add_argument("--debug", default=True, action="store_true", help="Debug mode")
    parser.add_argument(
        "--explicit", dest="debug", action="store_false", help="Explicit mode"
    )

    args: argparse.Namespace = parser.parse_args()

    # Specify default values for args in debug mode
    debug_defaults: Dict[str, Any] = {
        "requiredstr": "Default str",
        "requiredint": 14,
        "optionalint": 10,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args
