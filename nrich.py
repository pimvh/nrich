#!/usr/bin/env python3 

"""
__author__ = "Pim van Helvoirt"
__copyright__ = "No Copyright 2022"
__credits__ = ["John Matherly", "Shodan"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Pim van Helvoirt"
__email__ = "pim.van.helvoirt@home.nl"
__status__ = "Production"

"""
import asyncio
import argparse
import ipaddress

import logging
import sys

import json
import aiohttp

logger = logging.getLogger()
# logging.basicConfig(level=logging.DEBUG)

SHODAN_URL = "https://internetdb.shodan.io/"

class ShodanLookupper():
    def __init__(self, ip_addrs : asyncio.Queue, 
                 output_file, output_type,
                 skipmissing) -> None:
        self.shodan_url = SHODAN_URL
        self.ips : asyncio.Queue = ip_addrs
        self.output_file = output_file
        self.output_type = output_type
        self.skipmissing = skipmissing

    async def look_up_ips(self):
        """ look up an IP from shodan """

        first = True

        if self.output_file:   
            f = open(self.output_file, "w+")

            if self.output_type == 'json':
                f.write('[')

        else:
            f = None

        async with aiohttp.ClientSession() as session:
             
            while not self.ips.empty():

                try:
                    ip = self.ips.get_nowait()
                    resp = await session.get(self.shodan_url + ip,
                                             headers={'User-Agent': 'nrich'})
                
                    resp = await resp.json()

                    if self.skipmissing:
                        if details := resp.get('detail'):
                            # IPs with no info look like this
                            # {'detail': 'No information available'}
                            if details.startswith('No info'):
                                continue 

                    if self.output_type == 'str':
                        for key, value in resp.items():
                            
                            if key == 'hostnames':
                                tabs = '\t'
                            else:
                                tabs = '\t\t'
                            print(f"{key}{tabs}{value}", file=f)
                        print('\n\n', file=f)
                    else:
                        # handle JSON
                        if first:
                            first = False
                        else:
                            f.write(',')

                        json.dump(resp, f)

                except json.JSONDecodeError:
                    logger.warning('Value error reading from JSON from Shodan request.')
                    continue
                except (aiohttp.ClientConnectionError, aiohttp.ClientResponseError) as exc:
                    logger.warning('aioHTTP error: %s', exc)
                    continue 
                except (KeyError, ValueError) as exc:
                    logger.warning('Value error reading from Shodan request: %s', exc)
                    continue
                except asyncio.QueueEmpty as exc:
                    logger.warning('AsyncIO Queue Error: %s', exc)
                    break

                finally:
                    self.ips.task_done()   

            if self.output_type == 'json':
                f.write(']')

            if f:
                f.close()                 


async def ip_reader(ip_file, queue : asyncio.Queue):
    """ ip reader """

    with ip_file as f:
        ips : list = f.readlines()

        for ip in ips:

            try: 
                network = ipaddress.ip_network(ip.strip())

                for ip in network:                
                    queue.put_nowait(str(ip))

            except ValueError:
                continue
    

async def main(tasks : list):
    """ main function to retrieve IP information from the shodan internetdb
        written in asyncio to speed up the requests.
        takes task list as argument to properly handle keyboard interrupts.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-input-file', '-i', type=argparse.FileType('r'), 
                        default=(None if sys.stdin.isatty() else sys.stdin),
                        help="File to parse IPs from, if not given parse from stdin")
    parser.add_argument('-output-file', '-o', type=str, help="file to write IPs to",
                        default=None)
    parser.add_argument('-output-type', '-t', choices=['json', 'str'], default='str',  
                        help='Format to output in')
    parser.add_argument('-skip_missing', '-s', default=True, help="skip IPs with no information on them.")
    parser.add_argument('-verbose', action="store_true", help="verbose output")

    args = parser.parse_args()

    if args.verbose:
        print('creating queue and IPlookup object...')

    queue = asyncio.Queue()
    ip_lookup = ShodanLookupper(queue, args.output_file, args.output_type) 
    
    if args.verbose:
        print('creating tasks...')

    input_task = asyncio.create_task(ip_reader(args.input_file, queue), name="IP inputter")
    lookup_task = asyncio.create_task(ip_lookup.look_up_ips(), name="IP lookupper")

    tasks = [input_task, lookup_task]

    # sleep shortly to avoid directly closing an empty queue.
    await asyncio.sleep(0.1)    
    await queue.join()

    # if args.output_file:
    #     with args.output_file as f:
    #         json.dump(ip_lookup.out, f)

    

    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":

    tasks = []

    try:
        asyncio.run(main(tasks))
    except KeyboardInterrupt as exc:

        if tasks:
            # Cancel our worker tasks.
            for task in tasks:
                task.cancel()