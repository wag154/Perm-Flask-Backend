from application.database import db 
from flask import request, make_response
from flask_restx import Namespace, Resource
from application.controllers.auth_middleware import token_required

api = Namespace("Kanban" , description= "Kanbans")

@api.produces("application/json")
@api.route("/details")
class Kanban_Details(Resource):

    @token_required
    def get (self, *args, **kwargs):
        pass

    @token_required
    def post (self, *args, **kwargs):
        pass