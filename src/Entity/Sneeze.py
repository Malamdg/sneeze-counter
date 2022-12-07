from datetime import datetime


class Sneeze:
    sneeze_id: int
    user_id: int
    create_time: datetime

    def __init__(self, sneeze_id, user_id, create_time):
        self.sneeze_id = sneeze_id
        self.user_id = user_id
        self.create_time = create_time if create_time is not None else datetime.now()

    def get_sneeze_id(self):
        return self.sneeze_id

    def get_user_id(self):
        return self.user_id

    def set_create_time(self, time: datetime):
        self.create_time = time
        return self

    def get_create_time(self):
        return self.create_time

