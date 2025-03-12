from fastapi.testclient import TestClient
from app.main import app
from app.models import Item

client = TestClient(app)

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    assert item["name"] == "Laptop"
    assert "price" in item

def test_read_item_with_query():
    response = client.get("/items/1?q=test")
    assert response.status_code == 200
    item = response.json()
    assert "test" in item["description"]

def test_read_nonexistent_item():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_create_item():
    new_item = {
        "id": 4,
        "name": "Monitor",
        "description": "Ultra-wide curved monitor",
        "price": 349.99,
        "tax": 70.0
    }
    response = client.post("/items/", json=new_item)
    assert response.status_code == 200
    assert response.json() == new_item

def test_create_existing_item():
    existing_item = {
        "id": 1,
        "name": "Test Laptop",
        "description": "This should fail",
        "price": 100.0,
        "tax": 20.0
    }
    response = client.post("/items/", json=existing_item)
    assert response.status_code == 400

def test_update_item():
    updated_item = {
        "id": 2,
        "name": "Updated Smartphone",
        "description": "Latest model with updates",
        "price": 799.99,
        "tax": 159.99
    }
    response = client.put("/items/2", json=updated_item)
    assert response.status_code == 200
    assert response.json() == updated_item

def test_delete_item():
    # First create an item to delete
    new_item = {
        "id": 5,
        "name": "Temporary Item",
        "description": "This will be deleted",
        "price": 10.0,
        "tax": 2.0
    }
    client.post("/items/", json=new_item)
    
    # Now delete it
    response = client.delete("/items/5")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}
    
    # Verify it's gone
    response = client.get("/items/5")
    assert response.status_code == 404