from datetime import datetime


def format_name(name: str):
    new_name = name
    spaces = name.__contains__(" ")
    composed = name.__contains__("-")

    if spaces:
        new_name = " ".join(map(lambda el: el.strip().capitalize(), new_name.strip().split(" ")))

    if composed:
        new_name = "-".join(map(lambda el: el.strip().capitalize(), new_name.strip().split("-")))

    return new_name


class Person:
    user_id: int
    first_name: str
    last_name: str
    age: int
    birthdate: datetime
    gender: str
    create_time: datetime

    def __init__(self, first_name, last_name, birthdate, age, gender, create_time):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.age = age
        self.gender = gender
        self.create_time = create_time if create_time is not None else datetime.now()

    def get_first_name(self):
        return format_name(self.first_name)

    def get_full_name(self):
        name = format_name(self.first_name)
        surname = self.last_name.strip().upper()
        return name + " " + surname

    def get_age(self):
        interval = datetime.now() - self.birthdate
        return interval.days // 365

    def get_birthdate(self):
        return self.birthdate
