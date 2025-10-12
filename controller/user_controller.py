from model.user import User
from model.data_base import DataBase
from model.utils.api_utils import ResponseHandler
from model.utils.validations_utils import Validations

class UserController:
    @staticmethod
    def create_user(user_name: str, email: str, password: str):
        validator = Validations(user_name, email, password)
        validation_response = validator.validate_user_data()

        if validation_response is not None:
            return ResponseHandler.error(
                message=validation_response,
                status_code=400
            )

        user = User(user_name, email, password)
        db = DataBase()
        try:
            db.create_table()
            result = db.insert_user(user.user_name, user.email, user.password_hash)
        finally:
            db.close()

        if result["success"]:
            return ResponseHandler.created(
                data=result["user"],
                message="User created successfully!"
            )
        else:
            return ResponseHandler.error(
                message=result["error"],
                status_code=400
            )

    @staticmethod
    def get_all_users():
        db = DataBase()
        try:
            users = db.get_all_users()
        finally:
            db.close()

        return ResponseHandler.success(data=users)

    @staticmethod
    def get_user_by_id(user_id):
        db = DataBase()
        try:
            user = db.get_user_by_id(user_id)
        finally:
            db.close()

        if user is None:
            return ResponseHandler.error(message="User not found", status_code=404)

        return ResponseHandler.success(data=user)

    @staticmethod
    def update_user(user_id, user_name=None, email=None, password=None):
        db = None
        try:
            db = DataBase()
            result = db.update_user(user_id, user_name, email, password)

            if not result["success"]:
                if "not found" in result["error"].lower():
                    return ResponseHandler.error(message="User not found", status_code=404)
                elif "already in use" in result["error"].lower():
                    return ResponseHandler.error(message="Email already in use", status_code=409)
                else:
                    return ResponseHandler.error(message="Email already in use", status_code=409)

            return ResponseHandler.success(data=result["user"], message="User updated successfully")

        except Exception as e:
            return ResponseHandler.error(message="Internal server error", details=str(e), status_code=500)
        finally:
            if db:
                db.close()

    @staticmethod
    def delete_user(user_id: int):
        try:
            db = DataBase()
            deleted = db.delete_by_id(user_id)

            if not deleted:
                return ResponseHandler.error(message=f"User with id {user_id} not found.", status_code=404)

            return ResponseHandler.success(message="User deleted successfully.")
        except Exception as e:
            return ResponseHandler.error(message=f"Error deleting user: {str(e)}", status_code=500)
