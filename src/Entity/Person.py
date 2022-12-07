class Person:
    user_id: int
    first_name: str
    last_name: str
    age: int
    gender: str

    def __init__(self, first_name, last_name, age, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender

