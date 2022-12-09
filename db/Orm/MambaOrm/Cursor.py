import sqlite3
from db.Orm.MambaOrm.Connection import Connection
from db.Orm.MambaOrm.Query import Query


class Cursor:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.cursor = self.connection.con.cursor()

    def execute(self, query: Query):
        self.cursor.execute(query.statement, query.bindValues)
