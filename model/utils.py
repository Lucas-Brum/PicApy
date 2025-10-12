from flask import jsonify 

class Validations:
    def __init__(self, user, email, password):
        self.user = user
        self.email = email
        self.password = password

    def validate_user_data(self):
        if not self.user or not self.email or not self.password:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Required fields: user_name, email, password",
                    }
                ),
                400,
            )
        return None