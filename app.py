from flask import Flask
from view.users_routes import users_bp
from model.utils.api_utils import ResponseHandler

app = Flask(__name__)
app.register_blueprint(users_bp, url_prefix="/")

@app.errorhandler(Exception)
def handle_exception(e):
    return ResponseHandler.error(
        message="Unexpected error. Please contact support.",
        status_code=500,
        details=str(e)
    )

if __name__ == "__main__":
    app.run(debug=True)
