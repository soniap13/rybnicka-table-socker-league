from dataclasses import dataclass


@dataclass
class SingleLeagueMatch:
    win_player: str
    loose_player: str
    goal_balance: int


@dataclass
class DoubleLeagueMatch:
    win_player1: str
    win_player2: str
    loose_player1: str
    loose_player2: str
    goal_balance: int
