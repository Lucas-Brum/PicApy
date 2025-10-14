class User:
    def __init__(self, user_name: str, email: str, password: str):
        self._user_name = user_name
        self._email = email
        self._password_hash = password

    @property
    def user_name(self):
        return self._user_name

    @property
    def email(self):
        return self._email

    @property
    def password_hash(self):
        return self._password_hash

    def check_password(self, password: str) -> bool:
        return Security.verify_password(password, self._password_hash)
