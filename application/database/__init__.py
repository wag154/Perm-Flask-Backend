from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from werkzeug.security import generate_password_hash
db = SQLAlchemy()

def create_db():
    from application.model.model import User_Account , Perm_Org, Group_Resources ,Ind_Resource , Kanban_task
    db.create_all()

    try:
        admin_org = Perm_Org (org_name = "system admin")
        db.session.add(admin_org)
        db.session.commit()
        
        org_id = admin_org._dict()["id"]

        admin_group = Group_Resources(group_id = org_id, resource_group_name = "system admin")
        db.session.add(admin_group)
        db.session.commit()

        group_id = admin_group._dict()["id"]

        admin_account = User_Account(username ="T1Admin", password = generate_password_hash(os.getenv("Password"),  method = 'pbkdf2:sha256'), email ="admint1@yes.com",name = "Jack", level = 10, org_id = org_id, group_id= group_id )
        db.session.add(admin_account)
        db.session.commit()

        resource_instance = Ind_Resource(Parent_id = group_id, Kanban_name = "Test Kanban")
        db.session.add(resource_instance)
        db.session.commit()

        db.session.close()

    except Exception as e:
        
        print("failed to add T1 admin, admin already exists")
