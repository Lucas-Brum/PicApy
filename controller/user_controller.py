from typing import Any
from model.user import User
from model.user_model import UserSchema
from model.security.security import Security
from model.api.api_utils import ResponseHandler
from model.validations import Validations


class UserController:
    def __init__(self, db):
        self.db = db

    def create_user(self, user_name: str, email: str, password: str) -> Any:
        try:
            user_data = UserSchema(user_name=user_name, email=email, password=password)
        except Exception as e:
            return ResponseHandler.error(message=str(e), status_code=400)

        validator = Validations(user_name, password)
        validation_response = validator.validate_user_data()
        if validation_response:
            return ResponseHandler.error(
                message=validation_response["message"], status_code=400
            )

        hashed_password = Security.hash_password(user_data.password)

        new_user = User(user_data.user_name, user_data.email, hashed_password)

        try:
            self.db.create_table()
            result = self.db.insert_user(
                new_user.user_name, new_user.email, new_user.password_hash
            )
        finally:
            self.db.close()

        if result["success"]:
            return ResponseHandler.created(
                data=result["user"], message="User created successfully!"
            )
        else:
            return ResponseHandler.error(message=result["error"], status_code=400)

    def get_all_users(self) -> Any:
        try:
            users = self.db.get_all_users()
        finally:
            self.db.close()

        return ResponseHandler.success(data=users)

    def get_user_by_id(self, user_id) -> Any:
        try:
            user = self.db.get_user_by_id(user_id)
        finally:
            self.db.close()

        if user is None:
            return ResponseHandler.error(message="User not found", status_code=404)

        return ResponseHandler.success(data=user)

    def update_user(self, user_id, user_name=None, email=None, password=None) -> Any:
        try:
            result = self.db.update_user(user_id, user_name, email, password)

            if not result["success"]:
                if "not found" in result["error"].lower():
                    return ResponseHandler.error(
                        message="User not found", status_code=404
                    )
                elif "already in use" in result["error"].lower():
                    return ResponseHandler.error(
                        message="Email already in use", status_code=409
                    )
                else:
                    return ResponseHandler.error(
                        message="Email already in use", status_code=409
                    )

            return ResponseHandler.success(
                data=result["user"], message="User updated successfully"
            )

        except Exception as e:
            return ResponseHandler.error(
                message="Internal server error", details=str(e), status_code=500
            )
        finally:
            if self.db:
                self.db.close()

    def delete_user(self, user_id: int) -> Any:
        try:
            deleted = self.db.delete_by_id(user_id)

            if not deleted:
                return ResponseHandler.error(
                    message=f"User with id {user_id} not found.", status_code=404
                )

            return ResponseHandler.success(message="User deleted successfully.")
        except Exception as e:
            return ResponseHandler.error(
                message=f"Error deleting user: {str(e)}", status_code=500
            )
