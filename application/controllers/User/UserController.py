from flask import current_app
from application.database import db
from application.model.model import User_Account
from flask import jsonify, request , make_response
from flask_restx import Namespace, Resource
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from application.controllers.auth_middleware import token_required

api = Namespace('username', description='user account')

@api.produces("application/json")
@api.route("/perm")
class Account_Perm(Resource):
     @token_required
     def put (self, *args, **kwargs):
          
          data = request.json

          Username = data.get("username")
          Permission = data.get("permission")

          if not all ([Username, Permission]):
               
               return {"Requirement issues": "requires information"}
          
          try :
               user_account = User_Account.query.filter_by(id = kwargs["user_id"]).first()
               
               perm_level = (user_account._dict())["level"]
               
               if not (perm_level > Permission):
                    return {"Requirement issues", "Too Low Level"},401
               
               update_account = User_Account.query.filter_by(username = Username).first()
               update_account.level = int(perm_level)

               return {"message" :"Successfully updated perms"},200
          
          except Exception as e:
               
               return {"message" : str(e)}

          

@api.produces('application/json')
@api.route("/login")
class User_Login(Resource):
    def post (self):
        try:
            data = request.json
            Username = data.get("username")
            Password = data.get("password")

            if not all ([Username,Password]):
 
                   return {"Requirement issues": "requires information"},404
        
            get_account = User_Account.query.filter_by(username = Username).first()

            if not get_account:
                return {"Account issue": "No account with that username"}, 404
            
            try:
                 
               account_details = get_account._dict()
               account_id = account_details["id"]

            except Exception as e:
                 
                 print(str(e))

            try:
                new_exp_time = datetime.utcnow() + timedelta(days=30)

                token = jwt.encode({"user_id": account_id, "exp" : new_exp_time}, 
                               current_app.config["SECRET_KEY"],
                               algorithm="HS256")

            except Exception as e:
                 return {"Error" : str(e)},500
               
            if check_password_hash(account_details["password"] ,Password):
                 
                 response = make_response({"Sign in": "passed"})
                 response.set_cookie('auth_token',token, httponly = True) 

                 return response
            
            else:
                 return {"Sign in": "Password incorrect"},401
            
        except Exception as e:
            
            print(str(e))

            return {"message" :str(e)},500
        
@api.produces('application/json')
@api.route("/new")       
class Create_account(Resource):    
    def post (self):
         try:
              data = request.json
              print(data)
              Username = data.get("username") 
              Password = data.get("password")
              Email = data.get("email")
              Name = data.get("name")

              if not all ([Username,Password,Email]):
                   return {"Requirement issues": "requires information"},404
              
              hashed_password = generate_password_hash(Password, method = 'pbkdf2:sha256')
              new_account = User_Account(username = Username, password = hashed_password, email = Email , name = Name if Name is not None else None)
              
              try:
                    db.session.add(new_account)
                    db.session.commit()
                    db.session.close()

          
              except Exception as e:
                    print(e)
                    if isinstance(e, IntegrityError) and ("UniqueViolation" in str(e) or "IntegrityError" in str(e)):
                         print(e)
                         return {"Requirement issues": "email address or username not unique"}, 400
                    else:
                         return {"Requirement issues": "Integrity error occurred"}, 400
                    
              return {"message": "added content"}, 200
         
         except Exception as e:
         
              return {"Error" : str(e)},500
