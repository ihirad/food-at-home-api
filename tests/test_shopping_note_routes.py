def test_create_note(auth_client):
    # Act
    response = auth_client.post("/notes", json={"note": "carrot"})
    response_body = response.json
    shoppingnote = response_body["shoppingnote"]
    foodie = shoppingnote["foodie"]

    # Assert
    assert response.status_code == 201
    assert shoppingnote["id"] == 1
    assert shoppingnote["note"] == "carrot"
    assert foodie["id"] == 1
    assert foodie["username"] == "testuser"

def test_get_all_notes_with_no_records(auth_client):
    # Act
    response = auth_client.get("/notes")
    response_body = response.json

    # Assert
    assert response.status_code == 200
    assert response_body == {'shoppingnote': []} 

def test_update_note(auth_client, test_note):
    # Act
    response = auth_client.put(f"/notes/{test_note}", json={"note": "carrot"})

    # Assert
    assert response.status_code == 200
    assert response.json["note"] == "carrot"

def test_delete_note(auth_client, test_note):
    # Act
    response = auth_client.delete(f"/notes/{test_note}")

    # Assert
    assert response.status_code == 200
    assert response.json["message"] == f"Note {test_note} deleted"

def test_delete_note_not_found(auth_client):
    # Act
    response = auth_client.delete("/notes/100")
    response_body = response.json

    # Assert
    assert response.status_code == 404
    assert response_body == {
    "message": "ShoppingNote id 100 is not found"
}

    

    
    

