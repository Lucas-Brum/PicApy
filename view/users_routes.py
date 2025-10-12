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


@users_bp.get("/users")
def get_all_users():
    result = UserController.get_all_users()
    return result 


@users_bp.get("/users/<int:user_id>")
def get_user(user_id):
    result = UserController().get_user_by_id(user_id)
    return result


@users_bp.put("/users/<int:user_id>")
def update_user(user_id):
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaa')
    data = request.get_json(silent=True) or {}
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")

    result = UserController().update_user(user_id, user_name, email, password)
    return result

@users_bp.delete("/users/<int:user_id>")
def delete_user(user_id):
    result = UserController().delete_user(user_id)
    return result