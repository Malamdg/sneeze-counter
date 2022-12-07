import sqlite3


class Connection:
    def __init__(self, db: str):
        self.con = sqlite3.connect(db)
