from db.Orm.MambaOrm.Query import Query


class QueryBuilder:
    def __init__(self):
        self.statement = ""
        self.bindValues = {}

    def select(self, *columns: str):
        if "SELECT" in self.statement:
            return self
        statement = "SELECT "

        statement += ", ".join(columns)

        self.statement = statement
        return self

    def from_table(self, table: str):
        if "FROM" in self.statement:
            return self
        self.statement += f" FROM {table}"
        return self

    def join(self, **tables_on):
        for table, on in tables_on.items():
            self.statement += f" JOIN {table} ON {on}"
        return self

    def where(self, condition: str):
        if "WHERE" in self.statement:
            return self

        self.statement += f" WHERE {condition}"
        return self

    def and_where(self, *conditions):
        if not("WHERE" in self.statement):
            self.statement += f" WHERE {conditions[0]}"
            conditions = conditions[1:]

        for condition in conditions:
            self.statement += f" AND {condition}"

        return self

    def or_where(self, *conditions):
        if not ("WHERE" in self.statement):
            self.statement += f" WHERE {conditions[0]}"
            conditions = conditions[1:]

        for condition in conditions:
            self.statement += f" OR {condition}"

        return self

    def order_by(self, **orders):
        if not("ORDER BY" in self.statement):
            order = list(orders.keys())[0]
            asc_desc = orders[order]
            if asc_desc is None:
                asc_desc = "ASC"
            self.statement += f" ORDER BY {order} {asc_desc}"
            orders.pop(order)

        for order, asc_desc in orders.items():
            if asc_desc is None:
                asc_desc = "ASC"
            self.statement += f"{order} {asc_desc}, "

        self.statement = self.statement[0:-2]

        return self

    def build_query(self):
        query = Query(self.statement, self.bindValues)
        self.__init__()
        return query
