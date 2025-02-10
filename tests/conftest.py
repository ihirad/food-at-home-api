import sys
import os
import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.user import Foodie
from werkzeug.security import generate_password_hash

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client):
    user = Foodie(username="testuser", password=generate_password_hash("testpassword"))
    db.session.add(user)
    db.session.commit()

    
    login_response = client.post("/users/login", json={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200  

    return client  