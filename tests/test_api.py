import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200

def test_get_single_item(client):
    response = client.get('/inventory/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1

def test_add_inventory_item(client):
    new_item = {
        "product_name": "Test Product",
        "brand": "Test Brand",
        "quantity": 10,
        "barcode": "1234567890123",
        "price": 9.99
    }
    response = client.post('/inventory', json=new_item)
    assert response.status_code == 201

def test_update_inventory_item(client):
    update_data = {
        "quantity": 20
    }
    response = client.patch('/inventory/1', json=update_data)
    assert response.status_code == 200

def test_delete_inventory_item(client):
    response = client.delete('/inventory/2')
    assert response.status_code == 200
