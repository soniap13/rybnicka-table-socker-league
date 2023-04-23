from typing import List
import sys

from constants import POSSIBLE_GOAL_BALANCES
from league_database import LeagueDatabase
from match import DoubleLeagueMatch


def _is_line_correct(line: List[str], db: LeagueDatabase) -> bool:
    return all([len(line) == 5],
               line[-1] in POSSIBLE_GOAL_BALANCES,
               all([db.is_player_in_database(line[i]) for i in range(4)]))


def _load_dl_matches_from_file(file_name: str, db_name: str) -> None:
    league_db = LeagueDatabase(db_name)
    with open(file_name, 'r') as file:
        lines = file.readlines()
    for line in lines:
        record = line.split(" ")
        if not _is_line_correct(record, league_db):
            print(f"line '{record}' is incorrect")
            continue
        league_db.insert_double_league_match(DoubleLeagueMatch(None, *record[:4], int(record[-1])))
    league_db.close_connection()


if __name__ == '__main__':
    _load_dl_matches_from_file(sys.argv[0], 'database.db')
