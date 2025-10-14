from model.user import User
from typeguard import typechecked
from model.security.security import Security
from model.utils.api_utils import ResponseHandler
from model.utils.validations_utils import Validations

class UserController:
    def __init__(self, db):
        self.db = db

    @typechecked
    def create_user(self, user_name: str, email: str, password: str) -> any:
        validator = Validations(user_name, email, password)
        validation_response = validator.validate_user_data()

        if validation_response is not None:
            return ResponseHandler.error(
                message=validation_response["message"],
                status_code=400
            )

        hashed_password = Security.hash_password(password)

        new_user = User(user_name, email, hashed_password)
        
        try:
            self.db.create_table()
            result = self.db.insert_user(new_user.user_name, new_user.email, new_user.password_hash)
        finally:
            self.db.close()

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

    @typechecked
    def get_all_users(self) -> any:
        try:
            users = self.db.get_all_users()
        finally:
            self.db.close()

        return ResponseHandler.success(data=users)

    @typechecked
    def get_user_by_id(self, user_id) -> any:
        try:
            user = self.db.get_user_by_id(user_id)
        finally:
            self.db.close()

        if user is None:
            return ResponseHandler.error(message="User not found", status_code=404)

        return ResponseHandler.success(data=user)

    @typechecked
    def update_user(self, user_id, user_name=None, email=None, password=None) -> any:
        try:
            result = self.db.update_user(user_id, user_name, email, password)

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
            if self.db:
                self.db.close()

    @typechecked
    def delete_user(self, user_id: int) -> any:
        try:
            deleted = self.db.delete_by_id(user_id)

            if not deleted:
                return ResponseHandler.error(message=f"User with id {user_id} not found.", status_code=404)

            return ResponseHandler.success(message="User deleted successfully.")
        except Exception as e:
            return ResponseHandler.error(message=f"Error deleting user: {str(e)}", status_code=500)
