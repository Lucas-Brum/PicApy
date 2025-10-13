from model.data_base import DataBase
from controller.user_controller import UserController
from flask  import g

class Factory:
      @staticmethod
      def user_controller():
        if "db" not in g:
            g.db = DataBase()
            return UserController(g.db)
        