from flask import Flask, jsonify, request

import inventory
from openfoodfacts import fetch_product

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Inventory Management API"})


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory.get_all_items())


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_single_item(item_id):

    item = inventory.get_item(item_id)

    if item:
        return jsonify(item)

    return jsonify({"error": "Item not found"}), 404


@app.route("/inventory", methods=["POST"])
def add_inventory():

    new_item = request.json

    inventory.add_item(new_item)

    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory(item_id):

    updated = inventory.update_item(item_id, request.json)

    if updated:
        return jsonify(updated)

    return jsonify({"error": "Item not found"}), 404


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory(item_id):

    deleted = inventory.delete_item(item_id)

    if deleted:
        return jsonify({"message": "Item deleted"})

    return jsonify({"error": "Item not found"}), 404


@app.route("/product/<barcode>", methods=["GET"])
def get_product(barcode):

    product = fetch_product(barcode)

    if product:
        return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)