import re

class Validations:
    def __init__(self, user, email, password):
        self.user = user
        self.email = email
        self.password = password

    def validate_user_data(self):
        print(self.email, self.user, self.password)

        if not self.user or not self.email or not self.password:
            return{
                "success": False,
                "message": "Required fields: user_name, email, password",
            }
                
        
        if not re.match(r"^[A-Za-z0-9]{3,30}$", self.user):
            return{
                "success": False,
                "message": "Username must be alphanumeric and 3-30 characters long",
            }

        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, self.email):
            return {"success": False, "message": "Invalid email format"}

        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;':\",.<>\/?]).{8,}$"
        if not re.match(password_regex, self.password):
            return{
                "success": False,
                "message": "Password must be at least 8 characters long, "
                "include uppercase, lowercase, number and special character",
            }

        return None
