import re


class Validations:
    def __init__(self, user_name: str, email: str, password: str) -> None:
        self.user_name = user_name
        self.email = email
        self.password = password

    def validate_have_data(self) -> dict | None:
        if not self.user_name or not self.email or not self.password:
            return {
                "erro": {
                    "success": False,
                    "message": "Required fields: user_name, email, password",
                }
            }
        return None

    def validate_user_name(self) -> dict | None:
        if not re.match(r"^[A-Za-z0-9]{3,30}$", self.user_name):
            return {
                "erro": {
                    "success": False,
                    "message": "Username must be alphanumeric and 3-30 characters long",
                }
            }
        return None

    def validate_email(self) -> dict | None:
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, self.email):
            return {"erro": {"success": False, "message": "Invalid email format"}}
        return None

    def validate_password(self) -> dict | None:
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;':\",.<>\/?]).{8,}$"
        if not re.match(password_regex, self.password):
            return {
                "erro": {
                    "success": False,
                    "message": "Password must be at least 8 characters long, "
                    "include uppercase, lowercase, number and special character",
                }
            }
        return None

    def validate_user_data(self) -> dict | None:
        # Validação em ordem (short-circuit)
        have_data = self.validate_have_data()
        if have_data:
            return have_data["erro"]

        user_name_error = self.validate_user_name()
        if user_name_error:
            return user_name_error["erro"]

        email_error = self.validate_email()
        if email_error:
            return email_error["erro"]

        password_error = self.validate_password()
        if password_error:
            return password_error["erro"]

        return None
