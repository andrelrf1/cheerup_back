import fire_base
from models.diary import Diary


class User:
    user_id = None
    first_name = None
    last_name = None
    birth_date = None
    email = None
    password = None
    personality = None
    diary_id = None

    def create_user(self):
        if not (all([self.first_name, self.last_name, self.birth_date, self.email, self.password])):
            raise TypeError('Many attributes are empty')

        diary = Diary()
        diary_id = diary.create_diary()
        fire_base.create('users', {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'email': self.email,
            'password': self.password,
            'personality': {'data': 'empty'},
            'diary_id': diary_id
        })
        return True

    def get_user_by_id(self, user_id: str):
        result = fire_base.get_by_id('users', user_id)
        if result is None:
            return False

        values = list(result.values())
        self.user_id = user_id
        self.first_name = values[0]['first_name']
        self.last_name = values[0]['last_name']
        self.birth_date = values[0]['birth_date']
        self.email = values[0]['email']
        self.password = values[0]['password']
        return True

    def get_user_by_email(self, email: str):
        result = fire_base.get_by_param('users', 'email', email)
        if result is None:
            return False

        values = list(result.values())
        self.user_id = list(result.keys())[0]
        self.first_name = values[0]['first_name']
        self.last_name = values[0]['last_name']
        self.birth_date = values[0]['birth_date']
        self.email = values[0]['email']
        self.password = values[0]['password']
        self.personality = values[0]['personality']
        self.diary_id = values[0]['diary_id']
        return True

    def user_data(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'email': self.email,
        }

    def update_user(self):
        user_data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'email': self.email,
            'password': self.password,
            'personality': self.personality
        }
        fire_base.update('users', self.user_id, user_data)
        return True

    def delete_user(self):
        fire_base.delete('users', self.user_id)
        return True

    def add_personality(self):
        pass

    def update_personality(self):
        pass
