import os
import sqlite3


def _initialize_db(db_name: str) -> None:
    if os.path.exists(db_name):
        raise RuntimeError(f"{db_name} already exists")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE players (
        name TEXT PRIMARY KEY,
        starting_dl_points REAL,
        try_hard_factor REAL
        )""")
    cursor.execute(
        """CREATE TABLE single_league_matches (
        sl_id INTEGER PRIMARY KEY AUTOINCREMENT,
        winning_player TEXT,
        loser_player TEXT,
        goal_balance INTEGER
        )""")
    cursor.execute(
        """CREATE TABLE double_league_matches (
        dl_id INTEGER PRIMARY KEY AUTOINCREMENT,
        winning_player1 TEXT,
        winning_player2 TEXT,
        loser_player1 TEXT,
        loser_player2 TEXT,
        goal_balance INTEGER
        )""")
    conn.close()


if __name__ == '__main__':
    _initialize_db('database.db')
