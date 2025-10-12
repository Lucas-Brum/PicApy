from flask import Flask
from view.users_routes import users_bp

app = Flask(__name__)

app.register_blueprint(users_bp, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True)
