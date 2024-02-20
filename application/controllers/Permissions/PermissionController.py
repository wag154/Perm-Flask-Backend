from flask import jsonify, request , make_response
from flask_restx import Namespace, Resource
from application.controllers.auth_middleware import token_required
from application.model.model import User_Account , Perm_Org , Group_Resources ,Ind_Resource ,Resource_one , Resource_two, Resource_three ,Kanban_task ,Kanban_Column

api = Namespace('Permission' , description="permission handler")

@api.produces("application/json")
@api.route("/account")

class Account_Perm(Resource):

    @token_required    
    def get (self , *args, **kwargs):
        
        try:
           
            account_instance = User_Account.query.filter_by(id = kwargs["user_id"]).first()
            account_info = account_instance._dict()
            
            try :

              org_id = account_info["org_id"]

            except Exception as e:
                 
                 return {"Requirement issues":"user is not apart of any organisation"}, 401
          
            try:

               group_id = account_info["group_id"]

            except Exception as e:
                
                return  {"Requirement issues":"user is not apart of any group"}, 401

           
            org_instance = Perm_Org.query.filter_by(id = org_id).first()

            if not org_instance :
            
                return {"Org Issue" : "Org not longer exists"}
            
           
            group_instance  = Group_Resources.query.filter_by(id = group_id).first()

            if not group_instance:

                return {"Group Issue" : "Group No Longer Exists"}
            
           
            if account_info["level"] < 5 :

                return {"Admin" : "Org Admin"}
            
           
            group_name = group_instance._dict()["resource_group_name"]

            org_name = org_instance._dict()["org_name"]
            resources = Ind_Resource.query.filter_by(group_id = group_id).all()

            all_resources = [resource._dict() for resource in resources]

            response_content = [{"group_name" : group_name} , {"org_name" : org_name}]
            cookie_contents =[]
            
            for resource in  all_resources:

                match resource:

                    case {"resource_type" : 1}:

                        kanban_instance = Resource_one.query.filter_by(Parent_id = resource["id"]).first()
                        kanban_info = kanban_instance._dict()

                        # figure out len of tasks for future feature
                        
                        kanban_task_instance = Kanban_task.query.filter_by(Parent_id = kanban_info["id"]).all()

                        response_content.append({"kanban" : {"kanban_name" : kanban_info["name"]} })
                        cookie_contents.append({'kanban_id':str(kanban_info["id"])})
                                      
                    case {"resource_type" : 2}:
                        
                        announcement_instance = Resource_two.query.filter_by(Parent_id = resource["id"])
                        announcement_info = announcement_instance._dict()

                        response_content.append( {"announcement" : [announcement_info["content"], announcement_info["Owner_name"]]} )
           
            response = make_response(response_content)

            for cookie in cookie_contents:

                key = str(list(cookie.keys())[0])

                response.set_cookie(key, str(cookie[key]), httponly = True)
            
            return response

        except Exception as e:
           
            return  {"Error" : str(e)}, 404
            
    @token_required
    def post (self, *args, **kwargs):

        try:
            pass

        except Exception as e:
        
            return {"message" : str(e)}