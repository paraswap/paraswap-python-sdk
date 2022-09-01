from enum import IntEnum
from typing import TypeVar


class Network(IntEnum):
    Ethereum = 1
    Ropsten = 3
    Optimism = 10
    Bsc = 56
    Polygon = 137
    Fantom = 250
    Arbiturm = 42161
    Avalanche = 43114


T = TypeVar("T")

MapToNetwork = dict[Network, T]
