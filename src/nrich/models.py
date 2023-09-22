from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv6Address
from typing import Optional


@dataclass
class ShodanResult:
    """Dataclass that represents the returned result
    from the InternetDB"""

    ip: Optional[IPv4Address | IPv6Address] = None
    cpes: Optional[list[str]] = field(default_factory=list)
    hostnames: list[str] = field(default_factory=list)
    ports: list[int] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    vulns: list[str] = field(default_factory=list)
    detail: str = ""
    empty: bool = field(init=False)

    def __post_init__(self):
        if self.detail == "No information available":
            self.empty = True

        self.empty = False
