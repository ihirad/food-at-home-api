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
    app = create_app({"TESTING": True, "SECRET_KEY": "test_secret"})
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Create a test user in the database."""
    with app.app_context():
        user = Foodie(username="testuser", password=generate_password_hash("password"))
        db.session.add(user)
        db.session.commit()
        return user 

