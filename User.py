class User:

    def __init__(self, email, login, password):
        self.email = email
        self.login = login
        self.password = password

    @property
    def email(self):
        return '{}.{}@email.co'.format(self.email, self.last)

    @property
    def login(self):
        return '{} {}'.format(self.email, self.last)

    @property
    def password(self):
        return '{} {}'.format(self.email, self.last)