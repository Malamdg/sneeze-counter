from db.Orm.MambaOrm.Query import Query

# one motto here : KISS
keys_in_order = [
    "SELECT",
    "FROM",
    "JOIN",
    "WHERE",
    "GROUP BY",
    "HAVING",
    "ORDER BY"
]


class QueryBuilder:

    def __init__(self):
        self.statement = {}
        self.bindValues = {}

    def select(self, *columns: str):
        if not("SELECT" in self.statement.keys()):
            self.statement["SELECT"] = []

        for column in columns:
            self.statement["SELECT"].append(column)
        return self

    def from_table(self, table: str):
        if not("FROM" in self.statement.keys()):
            self.statement["FROM"] = []
        self.statement["FROM"].append(table)
        return self

    def join(self, **tables_on):
        if not("JOIN" in self.statement.keys() or "ON" in self.statement.keys()):
            self.statement["JOIN"] = []
            self.statement["ON"] = {}

        for table, on in tables_on.items():
            self.statement["JOIN"].append(table)
            self.statement["ON"][table] = on
        return self

    def where(self, condition: str, value=None):
        if not("WHERE" in self.statement.keys()):
            self.statement["WHERE"] = {}
        self.statement["WHERE"]["PRIMARY"] = {condition: value}
        return self

    def and_where(self, **conditions):
        if not("WHERE" in self.statement.keys()):
            cond = list(conditions.keys())[0]
            val = conditions[cond]
            self.where(condition=cond, value=val)
            self.statement["WHERE"]["AND"] = {}
            conditions.pop(cond)

        for column, value in conditions.items():
            self.statement["WHERE"]["AND"][column] = value

        return self

    def or_where(self, **conditions):
        if not("WHERE" in self.statement.keys()):
            cond = list(conditions.keys())[0]
            val = conditions[cond]
            self.where(condition=cond, value=val)
            self.statement["WHERE"]["OR"] = {}
            conditions.pop(cond)

        for column, value in conditions.items():
            self.statement["WHERE"]["OR"][column] = value

        return self

    def group_by(self, column: str):
        self.statement["GROUP BY"] = column
        return self

    def having(self, **conditions):
        if not("HAVING" in self.statement.keys()):
            self.statement["HAVING"] = {}

        for column, value in conditions.items():
            self.statement['HAVING'][column] = value
        return self

    def order_by(self, **orders):
        if not ("ORDER BY" in self.statement.keys()):
            self.statement["ORDER BY"] = {}

        for column, order in orders.items():
            if order is None:
                order = "ASC"
            self.statement["ORDER BY"][column] = order

        return self

    def parse_statement(self):
        parsed_statement = ""

        # Iterate on keys in order of apparition in correct sql statement
        # doesn't try to assert if statement is valid
        for key in keys_in_order:
            if not(key in self.statement.keys()):
                continue

            # Easy and generic case
            if key in ["SELECT", "FROM", "GROUP BY"]:
                parsed_statement += f"{key} "
                for col in self.statement[key]:
                    parsed_statement += f"{col}, "
                parsed_statement = parsed_statement[:-2]

            # Less easy but still simple, JOIN case
            if key == "JOIN":
                join = self.statement[key]
                ons = self.statement["ON"]

                for table in join:
                    on = ons[table]
                    parsed_statement += f" {key} {table} ON {on} "

                parsed_statement = parsed_statement[:-1]

            # Where case the most ""complicated""
            if key == "WHERE":
                where = self.statement[key]
                primary = where["PRIMARY"]
                primary_col = primary.keys().index(0)
                primary_val = primary[primary_col]

                parsed_statement += f" {key} {primary_col} "
                parsed_statement = self.bind_values(primary_val, parsed_statement)

                if "AND" in where.keys():
                    for col, value in where["AND"].items():
                        parsed_statement += f" AND {col} "
                        parsed_statement = self.bind_values(value, parsed_statement)

                if "OR" in where.keys():
                    for col, value in where["OR"].items():
                        parsed_statement += f" OR {col} "
                        parsed_statement = self.bind_values(value, parsed_statement)

            # Having case
            if key == "HAVING":
                having = self.statement[key]
                parsed_statement += f" {key} "
                for col, value in having.items():
                    parsed_statement += f" {col} "
                    parsed_statement = self.bind_values(value, parsed_statement)

            # Order by case
            if key == "ORDER BY":
                order_by = self.statement[key]
                parsed_statement += f" {key} "

                for col, order in order_by.items():
                    parsed_statement += f" {col} {order}, "

                parsed_statement = parsed_statement[:-2]

        return parsed_statement

    def bind_values(self, values, statement):
        i = self.bindValues.__len__() + 1
        if not (values is None):
            if isinstance(values, list):
                statement += '('
                for val in values:
                    bind_key = f":__{i}__"
                    self.bindValues[bind_key] = val
                    statement += f"{bind_key}, "
                    i += 1
                statement = statement[:-2] + ')'
            else:
                bind_key = f":__{i}__"
                self.bindValues[bind_key] = values
                statement += f"{bind_key} "
                i += 1
        return statement

    def build_query(self):
        query = Query(self.parse_statement(), self.bindValues)
        self.__init__()
        return query
