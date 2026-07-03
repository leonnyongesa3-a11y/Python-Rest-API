from unittest.mock import patch
import pytest
from app import fetch_products_by_barcode

@patch('app.requests.get')
def test_fetch_product_success(mock_get):

    mock_get.return_value.status_code = 200

    mock_get.return_value.json.return_value = {

        "status": 1,

        "product": {

            "product_name": "Nutella",
            "brands": "Ferrero",
            "ingredients_text":
                "Sugar, palm oil",

            "categories":
                "Spreads"
        }
    }

    result = fetch_products_by_barcode(
        "3017620422003"
    )

    assert result['product_name'] == (
        "Nutella"
    )
