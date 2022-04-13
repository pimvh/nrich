#!/usr/bin/env python3
import argparse
import json
import pprint
import sys

def main():
    """ program made to be able to parse shodan internet db output, which looks like this:
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
    parser.add_argument('-input-file', '-i', type=argparse.FileType('r'), 
                        default=(None if sys.stdin.isatty() else sys.stdin),
                        help="File to parse IPs from, if not given parse from stdin")
    parser.add_argument('-output-file', '-o', type=argparse.FileType('w+'), help="file to write IPs to",
                        default=None)

    with open('out.json') as f:
        shodan = json.load(f)
    
    for i, item in enumerate(shodan):

        if item.get('vulns'):
            pprint.pprint(item, '\n')

        if ip := item.get('ip'):
            if ip == 'YOUR IP':
               pprint.pprint(item, '\n') 

        if ports := item.get('ports'):
            if 3389 in ports:
               pprint.pprint(item, '\n') 

if __name__ == "__main__":
    main()