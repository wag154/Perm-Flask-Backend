from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv, find_dotenv
from application.model import model
from application.database import db , create_db

def create_app(env = None):
    app = Flask(__name__)
    
    if env == 'TEST':
        print("this is called")
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SECRET_KEY"] = "pass"
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    
    else :
        load_dotenv(find_dotenv())

        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DB")}'
        app.config["SECRET_KEY"] = "pass"
        app.config['TESTING'] = False

    db.init_app(app)
    
    with app.app_context():
        create_db()

        CORS(app,supports_credentials=True)
        
        from application.controllers import api 
        api.init_app(app)

        return app