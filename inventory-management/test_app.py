import unittest

from app import app


class InventoryTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_get_inventory(self):
        response = self.client.get("/inventory")
        self.assertEqual(response.status_code, 200)

    def test_get_single_item(self):
        response = self.client.get("/inventory/1")
        self.assertEqual(response.status_code, 200)

    def test_add_item(self):

        item = {
            "id": 10,
            "barcode": "12345",
            "product_name": "Milk",
            "brand": "Brookside",
            "price": 3.99,
            "stock": 5,
            "ingredients": "Milk"
        }

        response = self.client.post(
            "/inventory",
            json=item
        )

        self.assertEqual(response.status_code, 201)

    def test_update_item(self):

        response = self.client.patch(
            "/inventory/1",
            json={
                "price": 9.99
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_item(self):

        response = self.client.delete("/inventory/2")

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()