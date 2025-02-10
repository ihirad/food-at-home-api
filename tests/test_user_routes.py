# import pytest
# from app.models.user import Foodie
# from werkzeug.security import generate_password_hash
# from app.db import db

# def test_register_user(client):
#     response = client.post("/users/register", json={
#         "username": "testuser",
#         "password": "testpassword"
#     })
#     assert response.status_code == 201
#     assert "User" in response.json["message"]

# def test_register_user_missing_fields(client):
#     response = client.post("/users/register", json={"username": "testuser"})
#     assert response.status_code == 400
#     assert "Missing username or password" in response.json["message"]

# def test_login_user(client, app):
#     with app.app_context():
#         foodie = Foodie(username="testuser", password=generate_password_hash("testpassword"))
#         db.session.add(foodie)
#         db.session.commit()
    
#     response = client.post("/users/login", json={
#         "username": "testuser",
#         "password": "testpassword"
#     })
#     assert response.status_code == 200
#     assert "User" in response.json["message"]

# def test_login_invalid_credentials(client):
#     response = client.post("/users/login", json={
#         "username": "wronguser",
#         "password": "wrongpassword"
#     })
#     assert response.status_code == 401
#     assert "Invalid username or password" in response.json["message"]

# def test_logout_user(client):
#     response = client.get("/users/logout")
#     assert response.status_code == 200
#     assert "User logged out" in response.json["message"]

# def test_delete_user(client, app):
#     with app.app_context():
#         foodie = Foodie(username="deleteuser", password=generate_password_hash("testpassword"))
#         db.session.add(foodie)
#         db.session.commit()
#         user_id = foodie.id
    
#     response = client.delete(f"/users/{user_id}")
#     assert response.status_code == 200
#     assert f"User {user_id} deleted" in response.json["message"]