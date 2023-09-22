#!/usr/bin/env python3
import json
import pprint

PORTS_OF_INTEREST = {80, 443}


async def parse_internetdb(args):
    """program made to be able to parse shodan internet db output,
    which looks like this:
    {
     "cpes":        [],
     "hostnames":   ["dns.google"],
     "ip":          "8.8.8.8",
     "ports":       [53, 443],
     "tags":        [],
     "vulns":       []
    },

    """

    with open(args.input_file, "r") as f:
        for line in f.readlines():
            shodan = json.loads(line)

            if shodan.get("vulns"):
                pprint.pprint(shodan)

            if ip := shodan.get("ip"):
                if ip == "YOUR IP":
                    pprint.pprint(shodan)

            elif ports := shodan.get("ports"):
                if PORTS_OF_INTEREST & set(ports):
                    pprint.pprint(shodan)
