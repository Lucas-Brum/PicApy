from model.data_base import DataBase
from controller.user_controller import UserController
from flask import g
from typeguard import typechecked

class Factory:
    @staticmethod
    @typechecked
    def user_controller() -> UserController:
        if "db" not in g:
            g.db = DataBase()
        return UserController(g.db)
