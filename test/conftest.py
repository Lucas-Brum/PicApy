import sys
import pathlib
import pytest

PROJECT_DIR = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from app import app as flask_app
from model.data_base import DataBase

@pytest.fixture
def app():
    flask_app.config.update(TESTING=True)
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
