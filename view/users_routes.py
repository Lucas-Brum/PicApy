from flask import Blueprint, request
from factory import Factory
from typing import Any


# Create a blueprint for user routes
users_bp = Blueprint("users", __name__)


# Route to create a new user
@users_bp.post("/users")
def create_user() -> Any:
    # Get data sent in the request body
    data = request.get_json(silent=True) or {}
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")

    user_controller = Factory.user_controller()

    # Call the controller to create the user
    result = user_controller.create_user(user_name, email, password)
    return result


# Route to return all users
@users_bp.get("/users")
def get_all_users() -> Any:
    user_controller = Factory.user_controller()

    # Call the controller to fetch all users
    result = user_controller.get_all_users()
    return result


# Route to return a specific user by ID
@users_bp.get("/users/<int:user_id>")
def get_user(user_id: int) -> Any:
    user_controller = Factory.user_controller()

    # Call the controller to fetch the user by ID
    result = user_controller.get_user_by_id(user_id)
    return result


# Route to update an existing user by ID
@users_bp.put("/users/<int:user_id>")
def update_user(user_id: int) -> Any:
    # Get data sent in the request body
    data = request.get_json(silent=True) or {}
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")

    user_controller = Factory.user_controller()

    # Call the controller to update the user
    result = user_controller.update_user(user_id, user_name, email, password)
    return result


# Route to delete a user by ID
@users_bp.delete("/users/<int:user_id>")
def delete_user(user_id: int) -> Any:
    user_controller = Factory.user_controller()

    # Call the controller to delete the user
    result = user_controller.delete_user(user_id)
    return result
