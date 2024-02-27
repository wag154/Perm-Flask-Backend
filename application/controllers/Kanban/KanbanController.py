from application.database import db 
from flask import request, make_response
from flask_restx import Namespace, Resource
from application.model.model import Kanban_task , Ind_Resource, Resource_one , User_Account , Group_Resources,Kanban_Column
from application.controllers.auth_middleware import token_required

api = Namespace("Kanban" , description= "Kanbans")

def  get_kanban (user_id):
        
        user_instance = User_Account.query.filter_by(id = user_id).first()
        
        group_instance = Group_Resources.query.filter_by(id = user_instance._dict()["group_id"]).first()

        ind_group_resource = Ind_Resource.query.filter_by(group_id = group_instance._dict()["id"]).first()

        kanban = Resource_one.query.filter_by(Parent_id = ind_group_resource.dict()["id"]).first()
        return kanban

@api.produces("application/json")
@api.route("/details")
class Kanban_Details(Resource):

    @token_required
    def get (self, *args, **kwargs):
        
        user_id = kwargs["user_id"]
        
        kanban_instance = get_kanban(user_id)


        
    @token_required
    def post (self, *args, **kwargs):
        pass

@api.produces("application/json")
@api.route("/tasks")
class Kanban_Task(Resource):

    @token_required
    def post (self, *args, **kwargs):
        try :

            data = request.json
            order = data.get("order")
            content = data.get("content")

            if not all ([order,content]):
                return {"Requirement Issue": "missing 'order' or 'content'"},404

            task_instance = Kanban_task(order = order, content = content)

            db.session.add(task_instance)
            db.session.commit()

            return {"created" : "created task"}, 200
        except Exception as e:

            return {"error": str(e)}, 400

@api.produces("application/json")
@api.route("/column")
class Kanban_column(Resource):

    @token_required
    def get (self, *args, **kwargs):
        pass