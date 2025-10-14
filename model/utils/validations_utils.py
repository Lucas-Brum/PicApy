import re
from typing import List, Dict, Any


class Validations:
    def __init__(self, user_name: str, email: str, password: str) -> None:
        self.user_name = user_name
        self.email = email
        self.password = password

    def validate_have_data(self) -> Dict[str, Any] | None:
        """Verifica campos ausentes e retorna lista específica."""
        missing_fields: List[str] = []

        if not self.user_name:
            missing_fields.append("user_name")
        if not self.email:
            missing_fields.append("email")
        if not self.password:
            missing_fields.append("password")

        if missing_fields:
            fields_str = ", ".join(missing_fields)
            return {
                "success": False,
                "message": f"Missing required fields: {fields_str}",
            }
        return None

    def validate_user_name(self) -> Dict[str, Any] | None:
        if self.user_name and not re.match(r"^[A-Za-z0-9]{3,30}$", self.user_name):
            return {
                "success": False,
                "message": "Username must be alphanumeric and 3-30 characters long",
            }
        return None

    def validate_email(self) -> Dict[str, Any] | None:
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if self.email and not re.match(email_regex, self.email):
            return {"success": False, "message": "Invalid email format"}
        return None

    def validate_password(self) -> Dict[str, Any] | None:
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;':\",.<>\/?]).{8,}$"
        if self.password and not re.match(password_regex, self.password):
            return {
                "success": False,
                "message": "Password must be at least 8 characters long, "
                "include uppercase, lowercase, number and special character",
            }
        return None

    def validate_user_data(self) -> Dict[str, Any] | None:
        missing_error = self.validate_have_data()
        if missing_error:
            return missing_error

        username_error = self.validate_user_name()
        if username_error:
            return username_error

        email_error = self.validate_email()
        if email_error:
            return email_error

        password_error = self.validate_password()
        if password_error:
            return password_error

        return None  # All validate
