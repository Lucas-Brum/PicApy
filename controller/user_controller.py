from model.user import User
from model.data_base import DataBase
from model.api_utils import Response
from model.utils import Validations

class UserController:
    def create_user(self, user_name: str, email: str, password: str):
            validator = Validations(user_name, email, password)
            validation_response = validator.validate_user_data()

            if validation_response is not None:
                return validation_response

            user = User(user_name, email, password)

            db = DataBase()
            try:
                db.create_table()
                result = db.insert_user(user.user_name, user.email, user.password_hash)
            finally:
                db.close()

            if result["success"]:
                return Response.success(
                    data=result["user"], message="User created successfully!"
                )
            else:
                return Response.error(message=result["error"])
