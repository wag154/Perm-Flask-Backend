from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from werkzeug.security import generate_password_hash
db = SQLAlchemy()

def create_db():
    from application.model.model import User_Account , Perm_Org, Group_Resources ,Ind_Resource , Kanban_task ,Resource_one , Kanban_Column
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

        try:

            resource_instance = Ind_Resource(group_id = group_id, resource_type = 1, resource_name = "admin_system")
            db.session.add(resource_instance)
            db.session.commit()

            resource_id = resource_instance._dict()["id"]

            ind_resource_instance = Resource_one(Parent_id = resource_id, Kanban_name = "Kanban Admin")
            db.session.add(ind_resource_instance)
            db.session.commit()

            kanban_id = ind_resource_instance._dict()["id"]

            column_instance = Kanban_Column (Parent_id= kanban_id,name = "Test Column")
            db.session.add(column_instance)
            db.session.commit()

            column_id = column_instance._dict()["id"]

            task_instance_one = Kanban_task(Parent_id = column_id, order  = 1 , content = "test, order 1")
            task_instance_two = Kanban_task(Parent_id = column_id,order = 2, content = "test, order 2" )
            
            db.session.add(task_instance_one)
            db.session.add(task_instance_two)

            db.session.commit()

        except Exception as e:
            
            print(e)
        
        db.session.close()

    except Exception as e:
        
        print("failed to add T1 admin, admin already exists")
