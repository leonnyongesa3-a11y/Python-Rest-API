from unittest.mock import patch
import pytest
from cli import add_inventory_item

@patch('cli.requests.post')
@patch('builtins.input')
def test_cli_add_inventory_item(mock_input, mock_post):
    mock_input.side_effect = [
        "Test Product",  
        "Test Brand",
        "10",
        "1234567890123",
        "9.99"
    ]

    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {
        "message": "Item added successfully."
    }

    add_inventory_item()

    assert mock_post.called