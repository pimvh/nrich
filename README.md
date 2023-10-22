# Nrich

Python equivalent of the Rust [nrich](https://gitlab.com/shodan-public/nrich) program, developed by Shodan. Simple async Python program to interact with the Shodan InternetDB API.

In addition to the official tool, you can specify subnets, and this tool just unpacks them.

## Usage

`nrich --help`:

```
usage: nrich.py [-h] [-input-file INPUT_FILE] [-output-file OUTPUT_FILE] [-output-type {json,str}] [-skip_missing]

options:
  -h, --help            show this help message and exit
  -input-file INPUT_FILE, -i INPUT_FILE
                        File to parse IPs from, if not given parse from stdin
  -output-file OUTPUT_FILE, -o OUTPUT_FILE
                        file to write IPs to
  -output-type {json,str}, -t {json,str}
                        Format to output in
  -skip_missing, -s     skip IPs with no information on them.
```

### Standalone

To run this program as a standalone tool, run:

```
python3 -m nrich <your command>
```

For example, you can get the InternetDB information for a single IP, with the following command:

```
echo -e "<< your IP HERE>>\n" | python3 -m nrich
INFO:root:creating queue and IPlookup object...
INFO:root:creating tasks...
INFO:ShodanLookupper:Starting session...
INFO:root:running tasks...
INFO:ShodanLookupper:Got response: ShodanResult(ip=None, cpes=[], hostnames=[], ports=[], tags=[], vulns=[], detail='No information available', empty=False)...
{"ip": null, "cpes": [], "hostnames": [], "ports": [], "tags": [], "vulns": [], "detail": "No information available", "empty": false}
```

Any stdout piped input will be consumed by Shodan, when it is a file that contains IPs, line by line. Refer to the `--help` statement for usage when you want to consume files instead.

### parse_internetdb.py

Example script to parse the shodan internet.db output

## Installation

This package is available via PyPi. In order to install you can use the following command

```
pip install nrich
```

### Nix users

For users of nix a flake is avaible. Have a look at flake.nix for the targets.

If you just want a shell where the package is available, run:

```
nix develop
```

# License

GPLv3, see license.txt
