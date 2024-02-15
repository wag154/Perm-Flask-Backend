from application.database import db

class Perm_Org  (db.Model):
    __tablename__ = "permorg"
    id = db.Column (db.Integer, primary_key = True)
    org_name = db.Column (db.String(100), nullable = False, unique= True)


class User_Account(db.Model):
    __tablename__ = "useraccounts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=True, default="")
    level = db.Column(db.Integer,nullable = True, default =0)
    group_id = db.Column(db.Integer,db.ForeignKey("permorg.id"), nullable = True)
    

    def _dict(self):
        return {
            "id": self.id,
            "username":self.username,
            "password":self.password,
            "email":self.email,
            "name":self.name,
            "level" : self.level
        }

class Group_Resources(db.Model):
    __tablename__ = "groupresources"
    id = db.Column (db.Integer, primary_key = True)
    group_id = db.Column(db.Integer,db.ForeignKey("permorg.id"))
    resource_group_name = db.Column(db.String(200), nullable=False)

#individual
class Ind_Resource(db.Model):
    __tablename__ = "indresource"
    id = db.Column (db.Integer, primary_key = True)
    group_id = db.Column(db.Integer,db.ForeignKey("permgroups.id"))
    resource_type = db.Column (db.Integer, nullable = False)
    resource_name = db.Column (db.String(100), nullable = False)

#kanban
class Resource_one(db.Model):
    __tablename__  ="resourceone"
    id = db.Column (db.Integer, primary_key = True)
    Parent_id = db.Column(db.Integer,db.ForeignKey("indresource.id"))
    Kanban_name = db.Column(db.String(100), nullable = False)

class Kanban_task (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    Parent_id = db.Column(db.Integer,db.ForeignKey("resourceone.id"))
    order = db.Column(db.Integer, nullable = False)
    content = db.Column (db.String(100), nullable = False)
