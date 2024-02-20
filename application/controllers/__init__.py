from flask_restx  import Api

from application.controllers.User.UserController import api as user_controller
from application.controllers.Permissions.PermissionController import api as perm_controller
from application.controllers.Kanban.KanbanController import api as kanban_controller

api = Api (title = "My API")

api.add_namespace(user_controller, path='/user')
api.add_namespace(perm_controller, path = "/permission")
api.add_namespace(kanban_controller, path = "/kanban")