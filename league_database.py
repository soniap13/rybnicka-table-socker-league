import sqlite3
from typing import List, Optional, Tuple

from match import DoubleLeagueMatch, SingleLeagueMatch
from player import Player


class LeagueDatabase:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._cursor = self._conn.cursor()
        #self.initialize_db()

    def close_connection(self) -> None:
        self._conn.close()
    
    def initialize_db(self) -> None:
        self._cursor.execute(
            """CREATE TABLE players (
            name text,
            sl_points real,
            dl_points real,
            is_try_hard bool
            )""")
        self._cursor.execute(
            """CREATE TABLE single_league_matches (
            win_player text,
            loose_player text,
            goal_balance integer
            )""")
        self._cursor.execute(
            """CREATE TABLE double_league_matches (
            win_player1 text,
            win_player2 text,
            loose_player1 text,
            loose_player2 text,
            goal_balance integer
            )""")
        
    def insert_player(self, name: str, dl_points: float, is_try_hard: bool) -> None:
        with self._conn:
             self._cursor.execute(
                 "INSERT INTO players VALUES (:name, :sl_points, :dl_points, :is_try_hard)",
                 {'name': name, 'sl_points': 0, 'dl_points': dl_points, 'is_try_hard': is_try_hard})

    def get_player_names(self) -> List[str]:
        self._cursor.execute("SELECT name FROM players")
        return [record[0] for record in self._cursor.fetchall()]
    
    def get_players(self) -> List[Player]:
        self._cursor.execute("SELECT name, sl_points, dl_points FROM players")
        return [Player(*record) for record in self._cursor.fetchall()]
    
    def insert_single_league_match(
            self, win_player: str, loose_player: str, goal_balance: int) -> None:
        with self._conn:
             self._cursor.execute("INSERT INTO single_league_matches VALUES (:win_player, :loose_player, :goal_balance)",
                                  {'win_player': win_player, 'loose_player': loose_player, 'goal_balance': goal_balance})

    def get_single_league_matches(self, num: Optional[int] = None) -> List[SingleLeagueMatch]:
        self._cursor.execute("SELECT * FROM single_league_matches")
        records = self._cursor.fetchall() if num is None else self._cursor.fetchmany(num)
        return [SingleLeagueMatch(*record) for record in records]
    
    def insert_double_league_match(
            self, win_player1: str, win_player2: str, loose_player1: str, loose_player2: str,
            goal_balance: int) -> None:
        with self._conn:
             self._cursor.execute("INSERT INTO double_league_matches VALUES (:win_player1, :win_player2, :loose_player1, :loose_player2, :goal_balance)",
                                  {'win_player1': win_player1, 'win_player2': win_player2, 'loose_player1': loose_player1, 'loose_player2': loose_player2, 'goal_balance': goal_balance})

    def get_double_league_matches(self, num: Optional[int] = None) -> List[DoubleLeagueMatch]:
        self._cursor.execute("SELECT * FROM double_league_matches")
        records = self._cursor.fetchall() if num is None else self._cursor.fetchmany(num)
        return [DoubleLeagueMatch(*record) for record in records]

    def update_player_dl_points(self, name, new_points: float) -> None:
        with self._conn:
            self._cursor.execute("UPDATE players SET dl_points = :dl_points WHERE name = :name",
                                 {'dl_points': new_points, 'name': name})

    def get_player_dl_points(self, name: str) -> float:
        self._cursor.execute("SELECT dl_points FROM players WHERE name = :name",
                             {'name': name})
        return float(self._cursor.fetchone()[0])
