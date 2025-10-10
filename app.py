from flask import Flask, request
from api_utils import Validations, Response


app = Flask(__name__)

@app.post("/users")
def create_user():
    data = request.get_json(silent=True) or {}

    user = data.get("user")
    email = data.get("email")
    password = data.get("password")

    validator = Validations(user, email, password)
    validation_response = validator.validate_user_data()

    if validation_response:
        return validation_response
    
    response = Response(user, email)
    return response.create_response()


if __name__ == "__main__":
    app.run(debug=True)
