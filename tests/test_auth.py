import pytest
import json
from flask import g, session
from src.database import db, User


def test_registration(client, app):
    payload = json.dumps({
        "username": "Vinay1",
        "email": "v@g1.com",
        "password": "qwerty1234"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    client.post("/api/v1/auth/register", data=payload, headers=headers)
    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "v@g1.com"
    

def test_valid_login(client):
    payload = json.dumps({
        "email": "v@g1.com",
        "password": "qwerty1234"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    res = client.post("/api/v1/auth/login", data=payload, headers=headers)
    access_token = res.get_json()["user"]["access"]
    
    access_headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    response = client.get("/api/v1/bookmarks/", headers=access_headers)

    assert response.status_code == 200