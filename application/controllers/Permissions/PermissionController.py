from flask import jsonify, request
from flask_restx import Namespace, Resource
from application.controllers.auth_middleware import token_required
from application.model.model import User_Account , Perm_Org , Group_Resources ,Ind_Resource

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

            



            return {"Found" : account_info}


        except Exception as e:
           
            return  {"Error" : str(e)}
            
    @token_required
    def post (self, *args, **kwargs):

        try:
            pass

        except Exception as e:
        
            return {"message" : str(e)}