import requests

BASE_URL = "http://127.0.0.1:5000"


def menu():
    while True:

        print("\n====== Inventory Management ======")
        print("1. View Inventory")
        print("2. View Product by ID")
        print("3. Add Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Search OpenFoodFacts")
        print("7. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            response = requests.get(f"{BASE_URL}/inventory")
            print(response.json())

        elif choice == "2":
            item_id = input("Enter ID: ")
            response = requests.get(f"{BASE_URL}/inventory/{item_id}")
            print(response.json())

        elif choice == "3":

            product = {
                "id": int(input("ID: ")),
                "barcode": input("Barcode: "),
                "product_name": input("Product Name: "),
                "brand": input("Brand: "),
                "price": float(input("Price: ")),
                "stock": int(input("Stock: ")),
                "ingredients": input("Ingredients: ")
            }

            response = requests.post(
                f"{BASE_URL}/inventory",
                json=product
            )

            print(response.json())

        elif choice == "4":

            item_id = input("ID: ")

            updates = {
                "price": float(input("New Price: ")),
                "stock": int(input("New Stock: "))
            }

            response = requests.patch(
                f"{BASE_URL}/inventory/{item_id}",
                json=updates
            )

            print(response.json())

        elif choice == "5":

            item_id = input("ID: ")

            response = requests.delete(
                f"{BASE_URL}/inventory/{item_id}"
            )

            print(response.json())

        elif choice == "6":

            barcode = input("Barcode: ")

            response = requests.get(
                f"{BASE_URL}/product/{barcode}"
            )

            print(response.json())

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    menu()