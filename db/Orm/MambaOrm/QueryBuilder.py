from db.Orm.MambaOrm.Query import Query


class QueryBuilder:
    def __init__(self):
        self.statement = ""
        self.bindValues = {}

    def select(self, columns):
        if "SELECT" in self.statement:
            return self
        self.statement += "SELECT "

        for col in columns:
            self.statement += col+", "

        return self

    def build_query(self):
        query = Query(self.statement, self.bindValues)
        self.__init__()
        return query
