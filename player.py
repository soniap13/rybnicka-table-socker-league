from dataclasses import dataclass


@dataclass
class Player:
    name: str
    sl_points: float
    dl_points: float
    try_hard_factor: int
