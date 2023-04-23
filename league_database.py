from enum import Enum
import sqlite3
from typing import List, Optional

from match import DoubleLeagueMatch, SingleLeagueMatch


def calculate_moved_points(diff: float, bilans: int) -> float:
    return pow((diff / 2720 + 1.7), 7.25) * (bilans / 10 + 0.5)


def calculate_ratio(player1_points: float, player2_points: float) -> float:
    return player1_points / (player1_points + player2_points)


def calculate_diff(winning_player1_points: float, winning_player2_points: float,
                   loser_player1_points: float, loser_player2_points: float) -> float:
    return loser_player1_points + loser_player2_points - winning_player1_points - winning_player2_points


class Order(Enum):
    asc = 'ASC'
    desc = 'DESC'


class LeagueDatabase:
    def __init__(self, db_name: str):
        self._conn = sqlite3.connect(db_name)
        self._cursor = self._conn.cursor()
        self._calculate_dl_points()
        #self._load_dl_matches_from_file('dl_matches.txt')

    def close_connection(self) -> None:
        self._conn.close()

    def is_player_in_database(self, player: str) -> bool:
        self._cursor.execute("SELECT * FROM players WHERE name = :player",
                             {"player": player})
        return self._cursor.fetchone() is not None

    def insert_player(self, player: str) -> None:
        with self._conn:
             self._cursor.execute(
                 "INSERT INTO players VALUES (:name, :starting_dl_points, :try_hard_factor)",
                 {'name': player.name, 'starting_dl_points': player.dl_points, 'try_hard_factor': player.try_hard_factor})
        self._player_to_dl_points[player.name] = player.dl_points

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
        self._player_to_dl_points[new_name] = self._player_to_dl_points[old_name]
        del self._player_to_dl_points[old_name]

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
        self._update_dl_points_after_match(match)

    def get_double_league_matches(self, num: Optional[int] = None, order: Order = Order.desc) -> List[DoubleLeagueMatch]:
        if order == Order.desc:
            self._cursor.execute("SELECT * FROM double_league_matches ORDER BY dl_id DESC")
        else:
            self._cursor.execute("SELECT * FROM double_league_matches ORDER BY dl_id ASC")
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

    def update_player_starting_dl_points(self, name, new_points: float) -> None:
        with self._conn:
            self._cursor.execute("UPDATE players SET starting_dl_points = :starting_dl_points WHERE name = :name",
                                 {'starting_dl_points': new_points, 'name': name})
        self._calculate_dl_points()

    def get_player_starting_dl_points(self, name: str) -> float:
        self._cursor.execute("SELECT starting_dl_points FROM players WHERE name = :name",
                             {'name': name})
        return round(float(self._cursor.fetchone()[0]), 2)

    def get_player_sl_points(self, name: str) -> float:
        print(name)
        self._cursor.execute("DROP TABLE IF EXISTS player_recent_won_matches")
        self._cursor.execute("DROP TABLE IF EXISTS player_recent_lost_matches")
        self._cursor.execute("DROP TABLE IF EXISTS player_recent_matches")
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
            SELECT player, avg_score
            FROM (
                SELECT player, AVG(score) as avg_score
                FROM (
                    SELECT player, - goal_balance / 10.0 + (try_hard_factor - :player_try_hard_factor) - (goal_balance / (goal_balance - 0.000001)) * 0.5 + 0.5 as score
                    FROM player_recent_lost_matches
                    INNER JOIN players
                    ON player_recent_lost_matches.player = players.name
                    UNION ALL
                    SELECT player, goal_balance / 10.0 + 1 - (:player_try_hard_factor - try_hard_factor) + (goal_balance / (goal_balance - 0.000001)) * 0.5 - 0.5 as score
                    FROM player_recent_won_matches
                    INNER JOIN players
                    ON player_recent_won_matches.player = players.name)
                GROUP BY player)
            """,
            {"player_try_hard_factor": self.get_player_try_hard_factor(name), "name": name})
        print(self._cursor.fetchall())
        self._cursor.execute(
            """
            SELECT player, score
            FROM (
                SELECT player, - goal_balance / 10.0 + (try_hard_factor - :player_try_hard_factor) - (goal_balance / (goal_balance - 0.000001)) * 0.5 + 0.5 as score
                FROM player_recent_lost_matches
                INNER JOIN players
                ON player_recent_lost_matches.player = players.name
                UNION ALL
                SELECT player, goal_balance / 10.0 + 1 - (:player_try_hard_factor - try_hard_factor) + (goal_balance / (goal_balance - 0.000001)) * 0.5 - 0.5 as score
                FROM player_recent_won_matches
                INNER JOIN players
                ON player_recent_won_matches.player = players.name)
            """,
            {"player_try_hard_factor": self.get_player_try_hard_factor(name), "name": name})
        print(self._cursor.fetchall())
        self._cursor.execute(
            """
            SELECT AVG(avg_score)
            FROM (
                SELECT player, AVG(score) as avg_score
                FROM (
                    SELECT player, - goal_balance / 10.0 + (try_hard_factor - :player_try_hard_factor) - (goal_balance / (goal_balance - 0.000001)) * 0.5 + 0.5 as score
                    FROM player_recent_lost_matches
                    INNER JOIN players
                    ON player_recent_lost_matches.player = players.name
                    UNION ALL
                    SELECT player, goal_balance / 10.0 + 1 - (:player_try_hard_factor - try_hard_factor) + (goal_balance / (goal_balance - 0.000001)) * 0.5 - 0.5 as score
                    FROM player_recent_won_matches
                    INNER JOIN players
                    ON player_recent_won_matches.player = players.name)
                GROUP BY player)
            """,
            {"player_try_hard_factor": self.get_player_try_hard_factor(name), "name": name})
        all = self._cursor.fetchall()
        print(all)
        player_score = all[0][0]
        self._cursor.execute("DROP TABLE IF EXISTS player_recent_won_matches")
        self._cursor.execute("DROP TABLE IF EXISTS player_recent_lost_matches")
        self._cursor.execute("DROP TABLE IF EXISTS player_recent_matches")
        return 0 if player_score is None else round(player_score * 100, 2)
    
    def get_team_dl_points(self, player1: str, player2: str) -> float:
        self._cursor.execute("DROP TABLE IF EXISTS team_recent_won_matches")
        self._cursor.execute("DROP TABLE IF EXISTS team_recent_lost_matches")
        self._cursor.execute("DROP TABLE IF EXISTS team_recent_matches")
        self._cursor.execute(
            """
            CREATE TABLE team_recent_matches AS
            SELECT *
            FROM double_league_matches
            WHERE
                (loser_player1 = :player1 AND loser_player2 = :player2)
                OR (loser_player1 = :player2 AND loser_player2 = :player1)
                OR (winning_player1 = :player1 AND winning_player2 = :player2)
                OR (winning_player1 = :player2 AND winning_player2 = :player1)
            ORDER BY dl_id DESC
            LIMIT 10
            """,
            {"player1": player1, "player2": player2}
        )
        self._cursor.execute(
            """
            CREATE TABLE team_recent_lost_matches AS
            SELECT winning_player1 as player1, winning_player2 as player2, goal_balance
            FROM team_recent_matches
            WHERE
                (loser_player1 = :player1 AND loser_player2 = :player2)
                OR (loser_player1 = :player2 AND loser_player2 = :player1)
            """,
            {"player1": player1, "player2": player2}
        )
        self._cursor.execute(
            """
            CREATE TABLE team_recent_won_matches AS
            SELECT loser_player1 as player1, loser_player2 as player2, goal_balance
            FROM team_recent_matches
            WHERE
                (winning_player1 = :player1 AND winning_player2 = :player2)
                OR (winning_player1 = :player2 AND winning_player2 = :player1)
            """,
            {"player1": player1, "player2": player2}
        )
        self._cursor.execute(
            """
            SELECT AVG(avg_score)
            FROM (
                SELECT player1, player2, AVG(score) as avg_score
                FROM (
                    SELECT player1, player2, - goal_balance / 10.0 - (goal_balance / (goal_balance - 0.000001)) * 0.5 + 0.5 as score
                    FROM team_recent_lost_matches
                    UNION
                    SELECT player1, player2, goal_balance / 10.0 + 1 + (goal_balance / (goal_balance - 0.000001)) * 0.5 - 0.5 as score
                    FROM team_recent_won_matches)
                GROUP BY player1, player2)
            """)
        team_score = self._cursor.fetchone()[0]
        self._cursor.execute("DROP TABLE IF EXISTS team_recent_won_matches")
        self._cursor.execute("DROP TABLE IF EXISTS team_recent_lost_matches")
        self._cursor.execute("DROP TABLE IF EXISTS team_recent_matches")
        return 0 if team_score is None else round(team_score * 100, 2)

    def get_player_try_hard_factor(self, name: str) -> int:
        self._cursor.execute(
            "SELECT try_hard_factor FROM players WHERE name = :name", {"name": name})
        return self._cursor.fetchone()[0]

    def delete_dl_match(self, match_id: int) -> None:
        with self._conn:
            self._cursor.execute("DELETE FROM double_league_matches WHERE dl_id = :dl_id",
                                 {"dl_id": match_id})
        self._calculate_dl_points()

    def delete_sl_match(self, match_id: int) -> None:
        with self._conn:
            self._cursor.execute("DELETE FROM single_league_matches WHERE sl_id = :sl_id",
                                 {"sl_id": match_id})

    def get_player_dl_points(self, player: str) -> float:
        return round(self._player_to_dl_points[player], 2)
            
    def _update_player_dl_points(self, name: str, new_points: float) -> None:
        self._player_to_dl_points[name] = new_points

    def _update_dl_points_after_match(self, match: DoubleLeagueMatch) -> None:
        winning_player1_points = self.get_player_dl_points(match.winning_player1)
        winning_player2_points = self.get_player_dl_points(match.winning_player2)
        loser_player1_points = self.get_player_dl_points(match.loser_player1)
        loser_player2_points = self.get_player_dl_points(match.loser_player2)
        winning_player2_ratio = calculate_ratio(winning_player1_points, winning_player2_points)
        winning_player1_ratio = 1 - winning_player2_ratio
        loser_player1_ratio = calculate_ratio(loser_player1_points, loser_player2_points)
        loser_player2_ratio = 1 - loser_player1_ratio
        diff = calculate_diff(winning_player1_points, winning_player2_points, loser_player1_points, loser_player2_points)
        points_to_add = calculate_moved_points(diff, match.goal_balance)
        self._update_player_dl_points(match.winning_player1, winning_player1_points + winning_player1_ratio * points_to_add)
        self._update_player_dl_points(match.winning_player2, winning_player2_points + winning_player2_ratio * points_to_add)
        self._update_player_dl_points(match.loser_player1, loser_player1_points - loser_player1_ratio * points_to_add)
        self._update_player_dl_points(match.loser_player2, loser_player2_points - loser_player2_ratio * points_to_add)

    def _calculate_dl_points(self) -> None:
        self._player_to_dl_points = {player: self.get_player_starting_dl_points(player)
                                     for player in self.get_player_names()}
        for match in self.get_double_league_matches(order=Order.asc):
            self._update_dl_points_after_match(match)
