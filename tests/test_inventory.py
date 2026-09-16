from app import create_app
from app.extensions import db
from app.models import Inventory
import unittest

class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

#           First route: test_get_inventory

    def test_get_inventory(self):
        with self.app.app_context():
            inventory = Inventory(
                name="Test Part",
                price=25.99
            )

            db.session.add(inventory)
            db.session.commit()

        response = self.client.get("/inventory/")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Test Part")
        self.assertEqual(data[0]["price"], 25.99)

#           Second route: GET /inventory/<id>

    def test_get_inventory_item(self):
        with self.app.app_context():
            inventory = Inventory(
                name="Brake Pad",
                price=45.99
            )

            db.session.add(inventory)
            db.session.commit()

            inventory_id = inventory.id

        response = self.client.get(
            f"/inventory/{inventory_id}"
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["name"], "Brake Pad")
        self.assertEqual(data["price"], 45.99)

#           Third route: POST /inventory/

    def test_create_inventory(self):
        inventory_data = {
            "name": "New Part",
            "price": 75.50
        }

        response = self.client.post(
            "/inventory/",
            json=inventory_data
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data["name"], "New Part")
        self.assertEqual(data["price"], 75.50)

#           Fourth route: PUT /inventory/<id>

    def test_update_inventory(self):
        with self.app.app_context():
            inventory = Inventory(
                name="Old Part",
                price=25.99
            )

            db.session.add(inventory)
            db.session.commit()

            inventory_id = inventory.id

        update_data = {
            "name": "Updated Part",
            "price": 35.99
        }

        response = self.client.put(
            f"/inventory/{inventory_id}",
            json=update_data
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["name"], "Updated Part")
        self.assertEqual(data["price"], 35.99)

#               Fifth route: DELETE /inventory/<id>

    def test_delete_inventory(self):
        with self.app.app_context():
            inventory = Inventory(
                name="Delete Part",
                price=15.99
            )

            db.session.add(inventory)
            db.session.commit()

            inventory_id = inventory.id

        response = self.client.delete(
            f"/inventory/{inventory_id}"
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Inventory item deleted successfully"
        )