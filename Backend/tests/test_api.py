from app import app

client = app.test_client()


def test_get_inventory():

    response = client.get('/inventory')

    assert response.status_code == 200


def test_add_inventory_item():

    response = client.post(

        '/inventory',

        json={

            "product_name": "Nutella",

            "barcode": "3017620422003",

            "brand": "Ferrero",

            "quantity": 10,

            "price": 5.99
        }
    )

    assert response.status_code == 201