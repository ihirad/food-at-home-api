
def test_register_user(client, new_user):
    # Act
    response = client.post("/users/register", json=new_user)

    # Assert
    assert response.status_code == 201
    assert "User" in response.json["message"]

def test_register_user_missing_fields(client):
    # Act
    response = client.post("/users/register", json={"username": "testuser"})

    # Assert
    assert response.status_code == 400
    assert "Missing username or password" in response.json["message"]

def test_login_user(client, existing_user):
    # Act
    response = client.post("/users/login", json=existing_user)

    # Assert
    assert response.status_code == 200
    assert "User" in response.json["message"]

def test_login_invalid_credentials(client):
    # Act
    response = client.post("/users/login", json={
        "username": "wronguser",
        "password": "wrongpassword"
    })

    # Assert
    assert response.status_code == 401
    assert "Invalid username or password" in response.json["message"]


def test_logout_user(auth_client):
    # Act
    response = auth_client.get("/users/logout")

    # Assert
    assert response.status_code == 200
    assert "User logged out" in response.json["message"]


def test_delete_user(client, delete_user):
    # Act
    response = client.delete(f"/users/{delete_user}")

    # Assert
    assert response.status_code == 200
    assert f"User {delete_user} deleted" in response.json["message"]

def test_delete_user_not_found(auth_client):
    # Act
    response = auth_client.delete("/users/100")
    response_body = response.json
    
    # Assert
    assert response.status_code == 404
    assert response_body == {
    "message": "Foodie id 100 is not found"
}