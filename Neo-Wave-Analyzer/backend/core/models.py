from dataclasses import dataclass
from typing import Literal

@dataclass
class Candle:
    index: int
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

@dataclass
class Monomove:
    id: int
    direction: Literal["UP", "DOWN"]
    start_index: int
    end_index: int
    start_time: str
    end_time: str
    start_price: float
    end_price: float
    price_length: float
    time_duration: int