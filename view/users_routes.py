from flask import Blueprint, request
from controller.user_controller import UserController

users_bp = Blueprint("users", __name__)


@users_bp.post("/users")
def create_user():
    data = request.get_json(silent=True) or {}
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")

    result = UserController().create_user(user_name, email, password)

    return result


