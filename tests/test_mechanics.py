from app import create_app
from app.extensions import db
from app.models import Mechanic
import unittest

class TestMechanic(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

#       first route: GET /mechanics/

    def test_get_mechanics(self):
        with self.app.app_context():
            mechanic = Mechanic(
                first_name="Test",
                last_name="Mechanic",
                email="mechanic@example.com",
                phone="555-555-5555"
            )

            db.session.add(mechanic)
            db.session.commit()

        response = self.client.get("/mechanics/")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["first_name"], "Test")
        self.assertEqual(data[0]["last_name"], "Mechanic")

#   Sedond route: POST /mechanics/

    def test_create_mechanic(self):
        mechanic_data = {
            "first_name": "New",
            "last_name": "Mechanic",
            "email": "newmechanic@example.com",
            "phone": "555-123-4567"
        }

        response = self.client.post(
            "/mechanics/",
            json=mechanic_data
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data["first_name"], "New")
        self.assertEqual(data["last_name"], "Mechanic")
        self.assertEqual(data["email"], "newmechanic@example.com")

#       Third route: PUT /mechanics/<id>

    def test_update_mechanic(self):
        with self.app.app_context():
            mechanic = Mechanic(
                first_name="Old",
                last_name="Name",
                email="old@example.com",
                phone="555-111-1111"
            )

            db.session.add(mechanic)
            db.session.commit()

            mechanic_id = mechanic.id

        update_data = {
            "first_name": "Updated",
            "last_name": "Mechanic",
            "email": "updated@example.com",
            "phone": "555-222-2222"
        }

        response = self.client.put(
            f"/mechanics/{mechanic_id}",
            json=update_data
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["first_name"], "Updated")
        self.assertEqual(data["last_name"], "Mechanic")
        self.assertEqual(data["email"], "updated@example.com")

#           Fourth route: test delete mechanic

    def test_delete_mechanic(self):
        with self.app.app_context():
            mechanic = Mechanic(
                first_name="Delete",
                last_name="Me",
                email="delete@example.com",
                phone="555-333-3333"
            )

            db.session.add(mechanic)
            db.session.commit()

            mechanic_id = mechanic.id

        response = self.client.delete(
            f"/mechanics/{mechanic_id}"
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Mechanic deleted successfully"
        )