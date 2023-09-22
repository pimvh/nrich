# nrich.py

Python equivalent of the rust [nrich](https://gitlab.com/shodan-public/nrich) program, developed by Shodan. Simple async Python program to interact with the Shodan InternetDB API.

In addition to the official tool, you can specify subnets, and this tool just unpacks them.

## Usage

### nrich.py

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

### parse_internetdb.py

Example script to parse the shodan internet.db output

# Installation

Make a virtual environment and install dependencies, like so:

```
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Nix users

```
nix develop
```

# License

GPLv3, see license.txt
