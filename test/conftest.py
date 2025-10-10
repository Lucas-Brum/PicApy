# D:\Users\lucas.brum\code\PicApy\test\conftest.py
import os, sys, pathlib, pytest

TESTS_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_DIR = TESTS_DIR.parent  # ...\PicApy

# Garante que a raiz do projeto esteja no sys.path
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from app import app as flask_app  # agora funciona

@pytest.fixture
def app():
    flask_app.config.update(TESTING=True)
    yield flask_app

@pytest.fixture
def client(app):
    with app.test_client() as c:
        yield c
