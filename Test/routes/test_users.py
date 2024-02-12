from flask import url_for
from application.model.model import User_Account
import jwt

def test_create_user(app_with_db):
    with app_with_db:   
        url = url_for('username_create_account')
    
    response = app_with_db.post(url, json ={
        "username" :"test",
        "password":"test",
        "email": "test"
    })
    assert response.status_code == 200

def test_unique_details(app_with_db):
    
    url = url_for('username_create_account')

    response = app_with_db.post(url, json ={
        "username" :"username123",
        "password" :"pass",
        "email" : "email@email.com"
    })
    data = response.json

    assert response.status_code == 400
    assert "email address or username not unique" == data.get("Requirement issues")

def test_all_details(app_with_db):
    url = url_for('username_create_account')
    response = app_with_db.post(url, json ={
        "username" :"test",
        "password":"test"
    })
    assert response.status_code == 404

def test_login_details_accepted(app_with_db):
    url = url_for('username_user__login')

    response = app_with_db.post(url, json ={
        "username" :"username123",
        "password":"pass",
        "email": "email@email.com"
    })
    headers = response.headers.getlist('Set-Cookies')

    print(headers)
   
    assert response.status_code == 204

def test_raise_level(app_with_db):
    url = url_for('username')