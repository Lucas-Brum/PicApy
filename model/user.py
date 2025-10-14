class User:
    def __init__(self, user_name: str, email: str, password_hash: str) -> None:
        self._user_name = user_name
        self._email = email
        self._password_hash = password_hash

    @property
    def user_name(self) -> str:
        return self._user_name

    @property
    def email(self) -> str:
        return self._email

    @property
    def password_hash(self) -> str:
        return self._password_hash
