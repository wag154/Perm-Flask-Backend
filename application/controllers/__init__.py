from flask_restx  import Api

from application.controllers.User.UserController import api as user_controller
from application.controllers.TokenTest.TokenTestcontroller import api as TokenTest_controller

api = Api (title = "My API")

api.add_namespace(user_controller, path='/user')
api.add_namespace(TokenTest_controller, path="/test")