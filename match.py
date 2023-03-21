from dataclasses import dataclass


@dataclass
class SingleLeagueMatch:
    winning_player: str
    loser_player: str
    goal_balance: int


@dataclass
class DoubleLeagueMatch:
    winning_player1: str
    winning_player2: str
    loser_player1: str
    loser_player2: str
    goal_balance: int
