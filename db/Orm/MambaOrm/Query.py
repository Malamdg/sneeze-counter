class Query:
    def __init__(self, statement: str, bind_values: dict):
        self.statement = statement
        self.bindValues = bind_values
