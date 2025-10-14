from controller.user_controller import UserController
from model.data_base import DataBase
from typing import cast
from flask import g


class Factory:
    @staticmethod
    def user_controller() -> UserController:
        if "db" not in g:
            g.db = DataBase()

        db = cast(DataBase, g.db)

        return UserController(db)
