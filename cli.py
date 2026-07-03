import requests

BASE_URL = "http://127.0.0.1:5000"

def view_inventory():

    try:
        response = requests.get(f"{BASE_URL}/inventory")
        if response.status_code == 200:
            items = response.json()

            print("\n===== INVENTORY =====\n")

            for item in items:
                print(f"""
ID: {item['id']}
Product: {item['product_name']}
Brand: {item['brand']}
Quantity: {item['quantity']}
Barcode: {item['barcode']}
Price: {item['price']}
                """)

        else:
            print("Error: Unable to fetch inventory data.")

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API.")

def view_single_item():
    try:
        item_id = int(
            input("Enter item ID:")
        )

        response = requests.get(
            f"{BASE_URL}/inventory/{item_id}"
        )
        if response.status_code == 200:
            item = response.json()

            print("\n===== ITEM DETAILS =====\n")

            for key, value in item.items():
                print(f"{key}: {value}")

        else:
            print("Item not found.")

    except ValueError:
        print("Invalid ID.")

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API.")

def add_inventory_item():
    try:
        product_name = input("Enter product name: ").strip()
        brand = input("Enter brand: ").strip()
        quantity = int(input("Enter quantity: "))
        barcode = input("Enter barcode: ").strip()
        price = float(input("Enter price: "))

        if quantity <= 0 or price < 0:
            print("Quantity and price must be positive.")

            return
        
        data = {
            "product_name": product_name,
            "brand": brand,
            "quantity": quantity,
            "barcode": barcode,
            "price": price
        }
        response = requests.post(f"{BASE_URL}/inventory", json=data)

        if response.status_code == 201:
            print("\nItem added successfully.\n")

            print(response.json())

        else:
            print("Failed to add item.")

    except ValueError:
        print("Invalid input. Please enter valid data.")

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API.")

def update_inventory_item():
    try:
        item_id = int(input("Enter item ID to update: "))
        quantity_input = input("Enter new quantity: ")
        price_input = input("Enter new price: ")

        data = {}
        if quantity_input:
            data["quantity"] = int(quantity_input)
        if price_input:
            data["price"] = float(price_input)

        response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=data)

        if response.status_code == 200:
            print("\nItem updated successfully.\n")

            print(response.json())

        else:
            print("Failed to update item.")

    except ValueError:
        print("Invalid input. Please enter valid data.")

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API.")

def delete_inventory_item():
    try:
        item_id = int(input("Enter item ID to delete: "))

        response = requests.delete(f"{BASE_URL}/inventory/{item_id}")

        if response.status_code == 200:
            print("\nItem deleted successfully.\n")

        else:
            print("Failed to delete item.")

    except ValueError:
        print("Invalid input. Please enter a valid item ID.")

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API.")

def find_product_on_api():
    try:
        barcode = input("Enter product barcode: ").strip()

        response = requests.get(f"{BASE_URL}/product/barcode/{barcode}")

        if response.status_code == 200:
            product_data = response.json()

            print("\n===== PRODUCT DETAILS =====\n")

            for key, value in product_data.items():
                print(f"{key}: {value}")

        else:
            print("Product not found.")

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API.")

def main():
    while True:
        print("""
===== INVENTORY MANAGEMENT SYSTEM =====
1. View Inventory
2. View Single Item
3. Add Inventory Item
4. Update Inventory Item
5. Delete Inventory Item
6. Find Product on API
7. Exit
        """)
        choice = input("Select option: ").strip()

        if choice == "1":
            view_inventory()
        elif choice == "2":
            view_single_item()
        elif choice == "3":
            add_inventory_item()
        elif choice == "4":
            update_inventory_item()
        elif choice == "5":
            delete_inventory_item()
        elif choice == "6":
            find_product_on_api()
        elif choice == "7":
            print("Exiting application...")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

        


