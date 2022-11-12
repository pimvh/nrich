#!/usr/bin/env python3
import argparse
import json
import pprint
import sys


PORTS_OF_INTEREST = {80, 443}


def main():
    """program made to be able to parse shodan internet db output, which looks like this:
    {
     "cpes":        [],
     "hostnames":   ["dns.google"],
     "ip":          "8.8.8.8",
     "ports":       [53, 443],
     "tags":        [],
     "vulns":       []
    },

    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-input-file",
        "-i",
        type=str,
        default="out.json",
        help="File to parse IPs from, if not given parse from stdin",
    )
    # parser.add_argument('-output-file', '-o', type=argparse.FileType('w+'), help="file to write IPs to", default=None)
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        shodan = json.load(f)

    for i, item in enumerate(shodan):

        if item.get("vulns"):
            pprint.pprint(item)

        if ip := item.get("ip"):
            if ip == "YOUR IP":
                pprint.pprint(item)

        elif ports := item.get("ports"):
            if PORTS_OF_INTEREST & set(ports):
                pprint.pprint(item)


if __name__ == "__main__":
    main()
