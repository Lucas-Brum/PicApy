import re


class Validations:
    def __init__(self, user_name: str, password: str) -> None:
        self.user_name = user_name
        self.password = password

    def validate_user_name(self) -> dict | None:
        # Regex específico que Pydantic não cobre
        if self.user_name and not re.match(r"^[A-Za-z0-9]{3,30}$", self.user_name):
            return {
                "success": False,
                "message": "Username must be alphanumeric and 3-30 characters long",
            }
        return None

    def validate_password(self) -> dict | None:
        # Regex para senha forte
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;':\",.<>\/?]).{8,}$"
        if self.password and not re.match(password_regex, self.password):
            return {
                "success": False,
                "message": "Password must include uppercase, lowercase, number and special character",
            }
        return None

    def validate_user_data(self) -> dict | None:
        username_error = self.validate_user_name()
        if username_error:
            return username_error
        password_error = self.validate_password()
        if password_error:
            return password_error
        return None
