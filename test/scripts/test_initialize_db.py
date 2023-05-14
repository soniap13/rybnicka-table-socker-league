import os
import sqlite3

import pytest

from scripts.initialize_db import _initialize_db


TEST_DB_NAME = 'new_db.db'


def test_initilize_db_creates_database_with_tables():
    assert os.path.exists(TEST_DB_NAME) is False
    _initialize_db(TEST_DB_NAME)
    assert os.path.exists(TEST_DB_NAME) is True
    os.remove(TEST_DB_NAME)


def test_initialize_db_raises_error_if_database_exists():
    with open(TEST_DB_NAME, "w"):
        pass
    with pytest.raises(RuntimeError) as error:
        _initialize_db(TEST_DB_NAME)
        assert str(error.value) == f'{TEST_DB_NAME} already exists'
    os.remove(TEST_DB_NAME)
