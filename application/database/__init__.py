from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from werkzeug.security import generate_password_hash
db = SQLAlchemy()

def create_db():

    from application.model.model import User_Account
    db.create_all()

    try:
        admin_account = User_Account(username ="T1Admin", password = generate_password_hash(os.getenv("Password"),  method = 'pbkdf2:sha256'), email ="admint1@yes.com",name = "Jack", level = 10 )
        db.session.add(admin_account)
        db.session.commit()

    except Exception as e:
    
        print("failed to add T1 admin, admin already exists")
