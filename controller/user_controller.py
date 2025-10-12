from model.user import User
from model.data_base import DataBase
from model.utils.api_utils import Response
from model.utils import Validations

class UserController:
    @staticmethod
    def create_user(user_name: str, email: str, password: str):
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

    @staticmethod
    def get_all_users():
        db = DataBase()
        try:
            users = db.get_all_users()  # ← deve retornar uma lista de dicts
        finally:
            db.close()

        return users 

    @staticmethod       
    def get_user_by_id(user_id):
        db = DataBase()
        try:
            user = db.get_user_by_id(user_id)
        finally:
            db.close()

        if user is None:
            return {"error": "User not found"}, 404

        return user, 200
    

    @staticmethod
    def update_user(user_id, user_name=None, email=None, password=None):
        db = None
        try:
            db = DataBase()
            result = db.update_user(user_id, user_name, email, password)

            if not result["success"]:
                if "not found" in result["error"]:
                    return {"error": "User not found"}, 404
                elif "already in use" in result["error"]:
                    return {"error": "Email already in use"}, 409
                else:
                    return {"error": "Update failed"}, 500

            return result["user"], 200

        except Exception as e:
            return {"error": "Internal server error"}, 500

        finally:
            if db:
                db.close()


    def delete_user(self, user_id: int):
        try:
            db = DataBase()

            deleted = db.delete_by_id(user_id)

            if not deleted:
                return Response.error(f"User with id {user_id} not found.")

            return Response.success(message="User deleted successfully.")

        except Exception as e:
            return Response.error(f"Error deleting user: {str(e)}")