from application.database import db
from datetime import datetime

class Perm_Org  (db.Model):
    __tablename__ = "permorg"
    id = db.Column (db.Integer, primary_key = True)
    org_name = db.Column (db.String(100), nullable = False, unique= True)

    def  _dict(self):

        return {

            "id" : self.id,
            "org_name" : self.org_name

        }
    
class Group_Resources(db.Model):
    __tablename__ = "groupresources"
    id = db.Column (db.Integer, primary_key = True)
    group_id = db.Column(db.Integer,db.ForeignKey("permorg.id"))
    resource_group_name = db.Column(db.String(200), nullable=False)
    view_level = db.Column (db.Integer, nullable = True )

    def _dict(self):
        return{
            "id" : self.id,
            "parent_id" : self.group_id,
            "resource_group_name" : self.resource_group_name,
        }
    
    def compare(self, level):
    
        return (self.view_level < level)

class User_Account(db.Model):
    __tablename__ = "useraccounts"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=True, default="")
    level = db.Column(db.Integer,nullable = True, default =0)
    org_id = db.Column(db.Integer,db.ForeignKey("permorg.id"), nullable = True)
    group_id = db.Column(db.Integer,db.ForeignKey("groupresources.id"))

    def _dict(self):

        return {

            "id" : self.id,
            "username":self.username,
            "password":self.password,
            "email":self.email,
            "name":self.name,
            "level" : self.level,
            "org_id" : self.org_id,
            "group_id" : self.group_id

        }


#individual
class Ind_Resource(db.Model):
    __tablename__ = "indresource"
    id = db.Column (db.Integer, primary_key = True)
    group_id = db.Column(db.Integer,db.ForeignKey("groupresources.id"))
    resource_type = db.Column (db.Integer, nullable = False)
    resource_name = db.Column (db.String(100), nullable = False)

    def _dict(self):

        return {

            "id" : self.id,
            "name" : self.resource_name,
            "resource_type" : self.resource_type,

        }
    
#kanban
class Resource_one(db.Model):
    __tablename__  ="resourceone"
    id = db.Column (db.Integer, primary_key = True)
    Parent_id = db.Column(db.Integer,db.ForeignKey("indresource.id"))
    Kanban_name = db.Column(db.String(100), nullable = False)

    def _dict(self):
        return {
            "id" : self.id,
            "Parent_id" : self.Parent_id,
            "name" : self.Kanban_name
        }
class Kanban_Column (db.Model):
    __tablename__ = "kanbancolumn"
    id = db.Column (db.Integer, primary_key = True)
    Parent_id = db.Column(db.Integer,db.ForeignKey("resourceone.id"))
    name = db.Column (db.String(100), nullable = False)

    def _dict(self):
        return {
            "id" : self.id,
            "name" : self.name
        }

class Kanban_task (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    Parent_id = db.Column(db.Integer,db.ForeignKey("kanbancolumn.id"))
    order = db.Column(db.Integer, nullable = False)
    content = db.Column (db.String(100), nullable = False)

    def _dict(self):

        return {
        
            "id" : self.id,
            "Parent_id" : self.Parent_id,
            "order" : self.order,
            "content" : self.content

        }
# announcement
class Resource_two (db.Model):
    __tablename__ = "resourcetwo"
    id = db.Column(db.Integer, primary_key= True)
    Parent_id = db.Column(db.Integer,db.ForeignKey("indresource.id"))
    content = db.Column (db.String(255), nullable = False )
    Owner_name = db.Column (db.String(100), db.ForeignKey("useraccounts.username"))

# Calendar
class Resource_three(db.Model):
    __tablename__ = "resourcethree"
    id = db.Column(db.Integer, primary_key= True)
    Parent_id = db.Column(db.Integer,db.ForeignKey("indresource.id"))
    title = db.Column(db.String(100), nullable = False)
    start_date = db.Column (db.DateTime, nullable = False , default = datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable = True)