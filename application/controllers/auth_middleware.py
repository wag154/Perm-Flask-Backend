from functools import wraps
import jwt
from flask import request, abort, current_app
from flask_restx import reqparse
from application.model.model import User_Account

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('auth_token', location='cookies', required=False)
            parsed_args = parser.parse_args()

            token = parsed_args.get('auth_token') or None
            if token is None:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

            user_id = data["user_id"]
                 
            current_user = User_Account().query.filter_by(id =data["user_id"]).first()


            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
            kwargs['user_id'] = user_id
            return f(*args, **kwargs)

        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

    return decorated
