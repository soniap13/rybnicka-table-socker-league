from dataclasses import dataclass
from typing import Optional


@dataclass
class SingleLeagueMatch:
    id: Optional[int]
    winning_player: str
    loser_player: str
    goal_balance: int


@dataclass
class DoubleLeagueMatch:
    id: Optional[int]
    winning_player1: str
    winning_player2: str
    loser_player1: str
    loser_player2: str
    goal_balance: int
