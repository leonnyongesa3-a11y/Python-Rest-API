
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
app.config['TESTING'] = True

mock_products = [

    {
        "id": 1,
        "status": 1,
        "product": {
            "barcode": "3017620422003",
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text":
                "Filtered water, almonds, cane sugar",
            "categories": "Plant-based beverages",
            "quantity": "1L",
            "nutriscore_grade": "A",
            "image_url":
                "https://example.com/almond_milk.jpg"
        }
    },

    {
        "id": 2,
        "status": 1,
        "product": {
            "barcode": "7622210449283",
            "product_name": "Oreo Cookies",
            "brands": "Oreo",
            "ingredients_text":
                "Sugar, wheat flour, palm oil",
            "categories": "Biscuits and cookies",
            "quantity": "176g",
            "nutriscore_grade": "E",
            "image_url":
                "https://example.com/oreo.jpg"
        }
    }
]

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "barcode": "3017620422003",
        "brand": "Silk",
        "quantity": 15,
        "price": 4.99
    },

    {
        "id": 2,
        "product_name": "Oreo Cookies",
        "barcode": "7622210449283",
        "brand": "Oreo",
        "quantity": 30,
        "price": 2.50
    }
]

next_id = 3

def fetch_products_by_barcode(barcode):
    
    url = (f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json")
        
    response = requests.get(url)
    if response.status_code != 200:
        return {
            "error": "Unable to connect to API"
        }
    
    data = response.json()
    if data.get("status") != 1:
        return {
            "error": "Product not found"
        }
    product_data = data.get("product", {})
    return {
        "barcode": barcode,

        "product_name": product_data.get("product_name"),

        "brand": product_data.get("brands"),

        "categories": product_data.get("categories"),

        "quantity": product_data.get("quantity"),

        "nutriscore": product_data.get("nutriscore_grade"),

        "image_url": product_data.get("image_url")
    }

def enhance_inventory_item(item):
    product_data = fetch_products_by_barcode(item["barcode"])

    if "error" in product_data:
        return item
    
    enhanced_item = {
        **item,

        "ingredients": product_data.get("ingredients"),

        "categories": product_data.get("categories"),

        "nutriscore": product_data.get("nutriscore"),

        "image_url": product_data.get("image_url")
    }

    return enhanced_item

@app.route('/inventory', methods=['GET'])
def get_inventory():
    enhanced_inventory = []
    for item in inventory:
        enhanced_inventory.append(enhance_inventory_item(item))
    return jsonify(enhanced_inventory), 200

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            enhanced_item = enhance_inventory_item(item)
            return jsonify(enhanced_item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/inventory', methods=['POST'])
def add_inventory_item():

    global next_id
    data = request.get_json()

    required_fields = [
        "product_name",
        "barcode",
        "brand",
        "quantity",
        "price"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
        
    new_item = {
        "id": next_id,
        "product_name": data["product_name"],
        "barcode": data["barcode"],
        "brand": data["brand"],
        "quantity": data["quantity"],
        "price": data["price"]
    }   
    inventory.append(new_item)
    next_id += 1
    return jsonify({
        "message": "Item added successfully",
        "item": new_item
    }), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_inventory_item(item_id):
    data = request.get_json()
    for item in inventory:
        if item["id"] == item_id:
            item["product_name"] = data.get("product_name", item["product_name"])
            item["barcode"] = data.get("barcode", item["barcode"])
            item["brand"] = data.get("brand", item["brand"])
            item["quantity"] = data.get("quantity", item["quantity"])
            item["price"] = data.get("price", item["price"])
            return jsonify({
                "message": "Item updated successfully",
                "item": item
            }), 200
        
    return jsonify({"error": "Item not found"}), 404

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    global inventory
    for item in inventory:
        if item["id"] == item_id:
            inventory = [
                inventory_item 
                for inventory_item in inventory
                if inventory_item["id"] != item_id
            ]
            return jsonify({
                "message": "Item deleted successfully"}), 200
        
    return jsonify({"error": "Item not found"}), 404

@app.route('/products/barcode/<barcode>', methods=['GET'])
def get_product_by_barcode(barcode):
    product = fetch_products_by_barcode(barcode)

    if "error" in product:
        return jsonify(product), 404
    
    return jsonify(product), 200


if __name__ == '__main__':
    app.run(debug=True)