class User:
    user_id = None
    first_name = None
    last_name = None
    birth_date = None
    email = None
    token = None

    def __init__(self, user_id, first_name, last_name, birth_date, email, token):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.email = email
        self.token = token
