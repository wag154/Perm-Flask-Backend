from flask_restx import Namespace, Resource
from flask import request, make_response
from application.model.model import TestTable
from application.controllers.auth_middleware import token_required
from application.database import db

api = Namespace('token_test',description= "using this to test token function")

@api.produces('application/json')
@api.route("/")
class Token_Test(Resource):
    @token_required
    def get (self, *args, **kwargs):
       print("yeppe")
       return "passed"

    @token_required
    def post(self, *args, **kwargs):
        data = request.json
        
        content = data.get("content")

        if not content :
            return {"Requirement issues": "requires information"},404
        
        try :
            tcontent = TestTable(test_content = content)
            
            db.session.add(tcontent)
            db.session.commit()
            db.session.close()

            return {"message": "added content"},200
        
        except Exception as e:
            return {"Error": str(e)},400
            
        