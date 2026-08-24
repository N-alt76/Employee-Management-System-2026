import sqlite3
from contextlib import contextmanager

from config import DATABASE_PATH


@contextmanager
def get_connection():
	connection = sqlite3.connect(DATABASE_PATH)
	connection.row_factory = sqlite3.Row
	try:
		yield connection
		connection.commit()
	except Exception:
		connection.rollback()
		raise
	finally:
		connection.close()


def initialize_database():
	with get_connection() as connection:
		connection.execute(
			"""
			CREATE TABLE IF NOT EXISTS employees (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				email TEXT NOT NULL UNIQUE,
				department TEXT NOT NULL,
				role TEXT NOT NULL,
				salary REAL NOT NULL CHECK (salary >= 0),
				created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
			)
			"""
		)
