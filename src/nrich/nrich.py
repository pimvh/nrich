"""
__author__ = "pimvh"
__copyright__ = "No Copyright 2022"
__credits__ = ["John Matherly", "Shodan"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Pim van Helvoirt"
__email__ = "pim.van.helvoirt@home.nl"
__status__ = "Production"
"""
import argparse
import asyncio
import json
import logging
import os
from dataclasses import asdict
from io import TextIOWrapper
from ipaddress import ip_network

import aiohttp

from .models import ShodanResult

logger = logging.getLogger()
logging.basicConfig(level=os.getenv("LOGLEVEL", logging.INFO))

SHODAN_URL = "https://internetdb.shodan.io/"


class ShodanLookupper:
    """class that looks up IPs from shodan by opening the passed file, if it exist,
    and starting a HTTP session against Shodan's internet db.
    Retrieve all information"""

    def __init__(
        self, ip_addrs: asyncio.Queue, output_file, output_type, skipmissing
    ) -> None:
        """initialized passed params to attributes"""

        self.shodan_url = SHODAN_URL
        self.ips: asyncio.Queue = ip_addrs
        self.output_file = output_file
        self.output_type = output_type
        self.skipmissing = skipmissing
        self._logger = logging.getLogger("ShodanLookupper")

    async def look_up_ips(self):
        """open passed file if present, start a session and close the file, if present"""

        if self.output_file:
            with open(self.output_file, "w+") as f:
                await self.start_session(f)
        else:
            await self.start_session(None)

    async def output_str(self, output_file: TextIOWrapper, resp: ShodanResult):
        """helper to output str output of Shodan"""

        print(str(resp), file=output_file)
        print("\n\n", file=output_file)

    async def output_json(self, output_file: TextIOWrapper, resp: ShodanResult):
        """helper to output JSON output of Shodan"""

        print(json.dumps(asdict(resp)), file=output_file)

    async def start_session(self, output_file):
        """start a Session against Shodan's InternetDB,
        and retrieve information of IPs until the queue is empty"""

        self._logger.info("Starting session...")

        async with aiohttp.ClientSession() as session:
            while not self.ips.empty():
                try:
                    ip = self.ips.get_nowait()
                    resp = await session.get(
                        self.shodan_url + ip, headers={"User-Agent": "nrich"}
                    )

                    resp = ShodanResult(**await resp.json())

                    self._logger.info("Got response: %s...", resp)

                    if self.skipmissing:
                        if resp.empty:
                            continue

                    if self.output_type == "str":
                        await self.output_str(output_file, resp)
                    else:
                        await self.output_json(output_file, resp)

                except json.JSONDecodeError:
                    logger.warning("Value error reading from JSON from Shodan request.")
                    continue
                except (
                    aiohttp.ClientConnectionError,
                    aiohttp.ClientResponseError,
                ) as exc:
                    logger.warning("aioHTTP error: %s", exc)
                    continue
                except (KeyError, ValueError) as exc:
                    logger.warning("Value error reading from Shodan request: %s", exc)
                    continue
                except asyncio.QueueEmpty as exc:
                    logger.warning("AsyncIO Queue Error: %s", exc)
                    break

                finally:
                    self.ips.task_done()


async def ip_reader(ip_file, queue: asyncio.Queue):
    """read IPs from a file and put them on a Queue"""

    with ip_file as f:
        ips: list = f.readlines()

        for ip in ips:
            try:
                network = ip_network(ip.strip())

                for ip in network:
                    queue.put_nowait(str(ip))

            except ValueError:
                continue


async def nrich(args: argparse.Namespace):
    logger.info("creating queue and IPlookup object...")

    queue = asyncio.Queue()
    ip_lookup = ShodanLookupper(
        queue, args.output_file, args.output_type, args.skip_missing
    )

    logger.info("creating tasks...")

    input_task = asyncio.create_task(
        ip_reader(args.input_file, queue), name="IP inputter"
    )
    lookup_task = asyncio.create_task(ip_lookup.look_up_ips(), name="IP lookupper")

    tasks = [input_task, lookup_task]

    # sleep shortly to avoid directly closing an empty queue.
    await asyncio.sleep(0.1)

    logger.info("running tasks...")
    await queue.join()
    await asyncio.gather(*tasks, return_exceptions=True)
