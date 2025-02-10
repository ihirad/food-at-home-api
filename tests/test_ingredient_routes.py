import pytest
from app.models.ingredient import Ingredient
from app.db import db

def test_get_all_ingredients_no_data(auth_client):
    # Act
    response = auth_client.get("/ingredients")
    response_body = response.json

    # Assert
    assert response.status_code == 200
    assert "ingredients" in response_body
    assert response_body == {"ingredients": []}

def test_add_or_create_ingredient_without_name(auth_client):
    # Act
    response = auth_client.post("/ingredients", json={})
    response_body = response.json

    # Assert
    assert response.status_code == 400
    assert "message" in response_body
    assert response_body == {"message": "Missing required field: 'ingredient'"}


def test_get_all_ingredients(auth_client):
    # Act
    response = auth_client.get("/ingredients")
    # Assert
    assert response.status_code == 200
    assert "ingredients" in response.json
    assert isinstance(response.json["ingredients"], list)

def test_delete_ingredient_no_data(auth_client):
    # Act
    response = auth_client.delete("/ingredients/100")
    response_body = response.json

    # Assert
    # assert response.status_code == 404
    assert "message" in response_body
    assert response_body == {
    "message": "Ingredient id 100 is not found"
}

def test_delete_ingredient(auth_client, added_ingredient):
    # Act
    delete_response = auth_client.delete(f"/ingredients/{added_ingredient}")
    get_response = auth_client.get("/ingredients")

    # Assert
    assert delete_response.status_code == 200
    assert "message" in delete_response.json
    assert all(ingredient["id"] != added_ingredient for ingredient in get_response.json["ingredients"])

