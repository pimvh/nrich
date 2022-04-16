# nrich.py

Inspired on the [nrich](https://gitlab.com/shodan-public/nrich) tool developed by shodan, but alas that tool was in Rust.

Thus I have made a Python3 port of that tool, to make it more includable in other projects.

In addition to the official tool, you can specify subnets, and this tool just unpacks them.

# parse_internetdb.py

Example script to parse the shodan internet.db output, using simple for lopping and if-ing.

# Installation

Make a virtual environment and install dependencies, like so:

```
python3 -m venv venv 
source ./venv/bin/activate
pip install -r requirements.txt
```

# License
GPLv3, see license.txt