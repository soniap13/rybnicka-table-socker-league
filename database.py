import sqlite3
from typing import List, Optional, Tuple


class Database:
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
            points real
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
        
    def insert_player(self, name: str, points: float) -> None:
        with self._conn:
             self._cursor.execute("INSERT INTO players VALUES (:name, :points)", {'name': name, 'points': points})
    
    def get_player_names(self) -> List[str]:
        self._cursor.execute("SELECT name FROM players")
        return [record[0] for record in self._cursor.fetchall()]
    
    def get_players(self) -> List[Tuple[str, str, float]]:
        self._cursor.execute("SELECT * FROM players")
        return [(record[0], str(record[1])) for record in self._cursor.fetchall()]
    
    def insert_single_league_match(
            self, win_player: str, loose_player: str, goal_balance: int) -> None:
        with self._conn:
             self._cursor.execute("INSERT INTO single_league_matches VALUES (:win_player, :loose_player, :goal_balance)",
                                  {'win_player': win_player, 'loose_player': loose_player, 'goal_balance': goal_balance})

    def get_single_league_matches(self, num: Optional[int] = None):
        self._cursor.execute("SELECT * FROM single_league_matches")
        if num is None:
            return self._cursor.fetchall()
        return self._cursor.fetchmany(num)
    
    def insert_double_league_match(
            self, win_player1: str, win_player2: str, loose_player1: str, loose_player2: str,
            goal_balance: int) -> None:
        with self._conn:
             self._cursor.execute("INSERT INTO double_league_matches VALUES (:win_player1, :win_player2, :loose_player1, :loose_player2, :goal_balance)",
                                  {'win_player1': win_player1, 'win_player2': win_player2, 'loose_player1': loose_player1, 'loose_player2': loose_player2, 'goal_balance': goal_balance})

    def get_double_league_matches(self, num: Optional[int] = None):
        self._cursor.execute("SELECT * FROM double_league_matches")
        if num is None:
            return self._cursor.fetchall()
        return self._cursor.fetchmany(num)
    
    def update_player_points(self, name, new_points: float) -> None:
        with self._conn:
            self._cursor.execute("UPDATE players SET points = :points WHERE name = :name",
                                 {'points': new_points, 'name': name})

    def get_player_points(self, name: str) -> float:
        self._cursor.execute("SELECT points FROM players WHERE name = :name",
                             {'name': name})
        return float(self._cursor.fetchone()[0])
