import sqlite3
from typing import List, Optional

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
            name TEXT PRIMARY KEY,
            sl_points REAL,
            dl_points REAL,
            try_hard_factor INTEGER
            )""")
        self._cursor.execute(
            """CREATE TABLE single_league_matches (
            sl_league_id INTEGER PRIMARY KEY AUTOINCREMENT,
            win_player TEXT,
            loose_player TEXT,
            goal_balance INTEGER
            )""")
        self._cursor.execute(
            """CREATE TABLE double_league_matches (
            dl_league_id INTEGER PRIMARY KEY AUTOINCREMENT,
            win_player1 TEXT,
            win_player2 TEXT,
            loose_player1 TEXT,
            loose_player2 TEXT,
            goal_balance INTEGER
            )""")
        
    def insert_player(self, player: Player) -> None:
        with self._conn:
             self._cursor.execute(
                 "INSERT INTO players VALUES (:name, :sl_points, :dl_points, :try_hard_factor)",
                 {'name': player.name, 'sl_points':  player.sl_points,
                  'dl_points': player.dl_points, 'try_hard_factor': player.try_hard_factor})

    def get_player_names(self) -> List[str]:
        self._cursor.execute("SELECT name FROM players")
        return [record[0] for record in self._cursor.fetchall()]
    
    def get_players(self) -> List[Player]:
        self._cursor.execute("SELECT * FROM players")
        return [Player(*record) for record in self._cursor.fetchall()]
    
    def insert_single_league_match(self, match: SingleLeagueMatch) -> None:
        with self._conn:
             self._cursor.execute(
                """INSERT INTO single_league_matches(win_player, loose_player, goal_balance) VALUES 
                (:win_player, :loose_player, :goal_balance)""",
                {'win_player': match.win_player, 'loose_player': match.loose_player,
                 'goal_balance': match.goal_balance})

    def get_single_league_matches(self, num: Optional[int] = None) -> List[SingleLeagueMatch]:
        self._cursor.execute("SELECT * FROM single_league_matches ORDER BY sl_league_id DESC")
        records = self._cursor.fetchall() if num is None else self._cursor.fetchmany(num)
        return [SingleLeagueMatch(*record[1:]) for record in records]
    
    def insert_double_league_match(self, match: DoubleLeagueMatch) -> None:
        with self._conn:
             self._cursor.execute(
                """INSERT INTO double_league_matches(win_player1, win_player2, loose_player1, loose_player2, goal_balance) VALUES 
                (:win_player1, :win_player2, :loose_player1, :loose_player2, :goal_balance)""",
                {'win_player1': match.win_player1, 'win_player2': match.win_player2,
                 'loose_player1': match.loose_player1, 'loose_player2': match.loose_player2,
                 'goal_balance': match.goal_balance})

    def get_double_league_matches(self, num: Optional[int] = None) -> List[DoubleLeagueMatch]:
        self._cursor.execute("SELECT * FROM double_league_matches ORDER BY dl_league_id DESC")
        records = self._cursor.fetchall() if num is None else self._cursor.fetchmany(num)
        return [DoubleLeagueMatch(*record[1:]) for record in records]

    def update_player_dl_points(self, name, new_points: float) -> None:
        with self._conn:
            self._cursor.execute("UPDATE players SET dl_points = :dl_points WHERE name = :name",
                                 {'dl_points': new_points, 'name': name})

    def get_player_dl_points(self, name: str) -> float:
        self._cursor.execute("SELECT dl_points FROM players WHERE name = :name",
                             {'name': name})
        return float(self._cursor.fetchone()[0])

    def get_sl_score(self, player_name: str) -> float:
        self._cursor.execute(
            """
            SELECT SUM(avg_score) FROM(
                SELECT player, AVG(score)/10 as avg_score FROM(
                    SELECT win_player as player, -goal_balance as score FROM single_league_matches
                    WHERE loose_player = :name
                    UNION
                    SELECT loose_player as player, goal_balance as score FROM single_league_matches
                    WHERE win_player = :name)
                GROUP BY player)
            """,
            {"name": player_name}
        )
        #print(f"{player_name}: {self._cursor.fetchall()}")
        self._cursor.execute(
            """
            SELECT try_hard_factor FROM players WHERE name = :name
            """,
            {"name": player_name}
        )
        player_try_hard_factor = self._cursor.fetchone()[0]
        self._cursor.execute(
            """
            SELECT player, try_hard_factor2 - :try_hard_factor1  FROM (
            SELECT name as player, try_hard_factor as try_hard_factor2 FROM players WHERE name != :name
            )
            """,
            {"try_hard_factor1": player_try_hard_factor, "name": player_name}
        )
        #print(f"{player_name}: {self._cursor.fetchall()}")
        self._cursor.execute(
            """
            SELECT *
            FROM
                (SELECT win_player as player, -goal_balance as score FROM single_league_matches
                 WHERE loose_player = :name
                 UNION
                 SELECT loose_player as player, goal_balance as score FROM single_league_matches
                 WHERE win_player = :name) first
            INNER JOIN
                (SELECT player, try_hard_factor2 - :try_hard_factor1 as factor FROM
                    (SELECT name as player, try_hard_factor as try_hard_factor2 FROM players WHERE name != :name)
                ) second
            ON first.player=second.player
            """,
            {"try_hard_factor1": player_try_hard_factor, "name": player_name}) 
        print(f"{player_name}: {self._cursor.fetchall()}")
        return 0
