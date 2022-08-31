from typing import TypeVar
from enum import Enum

class Network(Enum):
    Ethereum = 1
    Ropsten = 3
    Optimism = 10
    Bsc = 56
    Polygon = 137
    Fantom = 250
    Arbiturm = 42161
    Avalanche = 43114

T = TypeVar('T')

MapToNetwork = dict[Network, T]
