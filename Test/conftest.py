import pytest
from application import create_app
from application.database import db
from sqlalchemy import delete
from application.model.model import User_Account
from werkzeug.security import generate_password_hash

@pytest.fixture(scope = "session")
def flask_app():
    
    app = create_app(env = 'TEST')

    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()

@pytest.fixture
def app_with_db(flask_app):

    db.session.query(User_Account).delete()
    db.session.commit()

    account = User_Account(username = "username123", password = generate_password_hash("pass"), email = "email@email.com")
    
    db.session.add(account)
    db.session.commit()

    yield flask_app

    db.session.remove()
