import argparse
import asyncio
import logging
import os
import sys

from .nrich import nrich
from .parse_internetdb import parse_internetdb

logger = logging.getLogger()
logging.basicConfig(level=os.getenv("LOGLEVEL", logging.INFO))


async def main(tasks: list):
    """main function to retrieve IP information from the shodan internetDB
    written in asyncio to speed up the requests.
    takes task list as argument to properly handle keyboard interrupts.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-input-file",
        "-i",
        type=argparse.FileType("r"),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help="File to parse IPs from, if not given parse from stdin",
    )
    parser.add_argument(
        "-output-file", "-o", type=str, help="file to write IPs to", default=None
    )
    parser.add_argument(
        "-output-type",
        "-t",
        choices=["json", "str"],
        default="json",
        help="Format to output in",
    )
    parser.add_argument(
        "-skip_missing",
        "-s",
        action="store_false",
        default=True,
        help="skip IPs with no information on them.",
    )

    parser.add_argument("-mode", "-m", choices=["nrich", "parse"], default="nrich")

    args = parser.parse_args()

    if args.mode == "nrich":
        await nrich(args)
    elif args.mode == "parse":
        await parse_internetdb(args)


if __name__ == "__main__":
    tasks = []

    try:
        asyncio.run(main(tasks))
    except KeyboardInterrupt:
        if tasks:
            # Cancel our worker tasks.
            for task in tasks:
                task.cancel()
