import sqlite3
from typing import List, Optional

from match import DoubleLeagueMatch, SingleLeagueMatch


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
            dl_points REAL,
            try_hard_factor REAL
            )""")
        self._cursor.execute(
            """CREATE TABLE single_league_matches (
            sl_id INTEGER PRIMARY KEY AUTOINCREMENT,
            winning_player TEXT,
            loser_player TEXT,
            goal_balance INTEGER
            )""")
        self._cursor.execute(
            """CREATE TABLE double_league_matches (
            dl_id INTEGER PRIMARY KEY AUTOINCREMENT,
            winning_player1 TEXT,
            winning_player2 TEXT,
            loser_player1 TEXT,
            loser_player2 TEXT,
            goal_balance INTEGER
            )""")

    def is_player_in_database(self, player: str) -> bool:
        self._cursor.execute("SELECT * FROM players WHERE name = :player",
                             {"player": player})
        return self._cursor.fetchone() is not None

    def insert_player(self, player: str) -> None:
        with self._conn:
             self._cursor.execute(
                 "INSERT INTO players VALUES (:name, :dl_points, :try_hard_factor)",
                 {'name': player.name, 'dl_points': player.dl_points, 'try_hard_factor': player.try_hard_factor})

    def update_player_name(self, old_name: str, new_name: str) -> None:
        with self._conn:
            self._cursor.execute(
                "UPDATE players SET name = :new_name WHERE name = :old_name",
                {"old_name": old_name, "new_name": new_name}
            )
            self._cursor.execute(
                "UPDATE single_league_matches SET winning_player = :new_name WHERE winning_player = :old_name",
                {"old_name": old_name, "new_name": new_name}
            )
            self._cursor.execute(
                "UPDATE single_league_matches SET loser_player = :new_name WHERE loser_player = :old_name",
                {"old_name": old_name, "new_name": new_name}
            )
            self._cursor.execute(
                "UPDATE double_league_matches SET winning_player1 = :new_name WHERE winning_player1 = :old_name",
                {"old_name": old_name, "new_name": new_name}
            )
            self._cursor.execute(
                "UPDATE double_league_matches SET winning_player2 = :new_name WHERE winning_player2 = :old_name",
                {"old_name": old_name, "new_name": new_name}
            )
            self._cursor.execute(
                "UPDATE double_league_matches SET loser_player1 = :new_name WHERE loser_player1 = :old_name",
                {"old_name": old_name, "new_name": new_name}
            )
            self._cursor.execute(
                "UPDATE double_league_matches SET loser_player2 = :new_name WHERE loser_player2 = :old_name",
                {"old_name": old_name, "new_name": new_name}
            )

    def update_player_try_hard_factor(self, player: str, new_try_hard_factor: float) -> None:
        with self._conn:
            self._cursor.execute("UPDATE players SET try_hard_factor = :new_try_hard_factor WHERE name = :player",
                                 {"new_try_hard_factor": new_try_hard_factor, "player": player})

    def get_player_names(self) -> List[str]:
        self._cursor.execute("SELECT name FROM players")
        return [record[0] for record in self._cursor.fetchall()]

    def insert_single_league_match(self, match: SingleLeagueMatch) -> None:
        with self._conn:
             self._cursor.execute(
                """INSERT INTO single_league_matches(winning_player, loser_player, goal_balance) VALUES 
                (:winning_player, :loser_player, :goal_balance)""",
                {'winning_player': match.winning_player, 'loser_player': match.loser_player,
                 'goal_balance': match.goal_balance})

    def get_single_league_matches(self, num: Optional[int] = None) -> List[SingleLeagueMatch]:
        self._cursor.execute("SELECT * FROM single_league_matches ORDER BY sl_id DESC")
        records = self._cursor.fetchall() if num is None else self._cursor.fetchmany(num)
        return [SingleLeagueMatch(*record) for record in records]

    def get_player_single_league_matches(self, player: str,
                                  num: Optional[int] = None) -> List[SingleLeagueMatch]:
        self._cursor.execute(
            """
            SELECT * FROM single_league_matches
            WHERE winning_player = :player OR loser_player = :player
            ORDER BY sl_id DESC
            """,
            {"player": player})
        records = self._cursor.fetchall() if num is None else self._cursor.fetchmany(num)
        return [SingleLeagueMatch(*record) for record in records]
    
    def insert_double_league_match(self, match: DoubleLeagueMatch) -> None:
        with self._conn:
             self._cursor.execute(
                """INSERT INTO double_league_matches(winning_player1, winning_player2, loser_player1, loser_player2, goal_balance) VALUES 
                (:winning_player1, :winning_player2, :loser_player1, :loser_player2, :goal_balance)""",
                {'winning_player1': match.winning_player1, 'winning_player2': match.winning_player2,
                 'loser_player1': match.loser_player1, 'loser_player2': match.loser_player2,
                 'goal_balance': match.goal_balance})

    def get_double_league_matches(self, num: Optional[int] = None) -> List[DoubleLeagueMatch]:
        self._cursor.execute("SELECT * FROM double_league_matches ORDER BY dl_id DESC")
        records = self._cursor.fetchall() if num is None else self._cursor.fetchmany(num)
        return [DoubleLeagueMatch(*record) for record in records]

    def get_player_double_league_matches(self, player: str,
                                         num: Optional[int] = None) -> List[DoubleLeagueMatch]:
        self._cursor.execute(
            """
            SELECT * FROM double_league_matches
            WHERE (winning_player1 = :player OR winning_player2 = :player
                   OR loser_player1 = :player OR loser_player2 = :player)
            ORDER BY dl_id DESC
            """,
            {"player": player})
        records = self._cursor.fetchall() if num is None else self._cursor.fetchmany(num)
        return [DoubleLeagueMatch(*record) for record in records]

    def update_player_dl_points(self, name, new_points: float) -> None:
        with self._conn:
            self._cursor.execute("UPDATE players SET dl_points = :dl_points WHERE name = :name",
                                 {'dl_points': new_points, 'name': name})

    def get_player_dl_points(self, name: str) -> float:
        self._cursor.execute("SELECT dl_points FROM players WHERE name = :name",
                             {'name': name})
        return round(float(self._cursor.fetchone()[0]), 2)

    def get_player_sl_points(self, name: str) -> float:
        self._cursor.execute(
            """
            CREATE TABLE player_recent_matches AS
            SELECT *
            FROM single_league_matches
            WHERE loser_player = :name OR winning_player = :name
            ORDER BY sl_id DESC
            LIMIT 10
            """,
            {"name": name}
        )
        self._cursor.execute(
            """
            CREATE TABLE player_recent_lost_matches AS
            SELECT winning_player as player, goal_balance
            FROM player_recent_matches
            WHERE loser_player = :name
            """,
            {"name": name}
        )
        self._cursor.execute(
            """
            CREATE TABLE player_recent_won_matches AS
            SELECT loser_player as player, goal_balance
            FROM player_recent_matches
            WHERE winning_player = :name
            """,
            {"name": name}
        )
        self._cursor.execute(
            """
            SELECT AVG(avg_score)
            FROM (
                SELECT player, AVG(score) as avg_score
                FROM (
                    SELECT player, - goal_balance / 10.0 + (try_hard_factor - :player_try_hard_factor) as score
                    FROM player_recent_lost_matches
                    INNER JOIN players
                    ON player_recent_lost_matches.player = players.name
                    UNION
                    SELECT player, goal_balance / 10.0 + 1 - (:player_try_hard_factor - try_hard_factor) as score
                    FROM player_recent_won_matches
                    INNER JOIN players
                    ON player_recent_won_matches.player = players.name)
                GROUP BY player)
            """,
            {"player_try_hard_factor": self.get_player_try_hard_factor(name), "name": name})
        player_score = self._cursor.fetchone()[0]
        self._cursor.execute("DROP TABLE IF EXISTS player_recent_won_matches")
        self._cursor.execute("DROP TABLE IF EXISTS player_recent_lost_matches")
        self._cursor.execute("DROP TABLE IF EXISTS player_recent_matches")
        return 0 if player_score is None else round(player_score * 100, 2)

    def get_player_try_hard_factor(self, name: str) -> int:
        self._cursor.execute(
            "SELECT try_hard_factor FROM players WHERE name = :name", {"name": name})
        return self._cursor.fetchone()[0]

    def delete_dl_match(self, match_id: int) -> None:
        with self._conn:
            self._cursor.execute("DELETE FROM double_league_matches WHERE dl_id = :dl_id",
                                 {"dl_id": match_id})

    def delete_sl_match(self, match_id: int) -> None:
        with self._conn:
            self._cursor.execute("DELETE FROM single_league_matches WHERE sl_id = :sl_id",
                                 {"sl_id": match_id})
