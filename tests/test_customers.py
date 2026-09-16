from app import create_app
from app.extensions import db, bcrypt
from app.models import Customer, ServiceTicket
import unittest


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_customers(self):
        with self.app.app_context():
            customer = Customer(
                first_name="Test",
                last_name="Customer",
                email="test@example.com",
                phone="555-555-5555",
                address="123 Test Street",
                password=bcrypt.generate_password_hash("testpassword").decode('utf-8')
            )

            db.session.add(customer)
            db.session.commit()

        response = self.client.get("/customers/")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["total"], 1)
        self.assertEqual(data["customers"][0]["first_name"], "Test")
        self.assertEqual(data["customers"][0]["email"], "test@example.com")

    def test_create_customer(self):
        customer_data = {
            "first_name": "New",
            "last_name": "Customer",
            "email": "newcustomer@example.com",
            "phone": "555-123-4567",
            "address": "456 New Street",
            "password": "testpassword"
        }

        response = self.client.post(
            "/customers/",
            json=customer_data
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data["first_name"], "New")
        self.assertEqual(data["last_name"], "Customer")
        self.assertEqual(data["email"], "newcustomer@example.com")

    def test_update_customer(self):
        with self.app.app_context():
            customer = Customer(
                first_name="Old",
                last_name="Name",
                email="old@example.com",
                phone="555-111-1111",
                address="111 Old Street",
                password=bcrypt.generate_password_hash("testpassword").decode('utf-8')
            )

            db.session.add(customer)
            db.session.commit()

            customer_id = customer.id

        update_data = {
            "first_name": "Updated",
            "last_name": "Customer",
            "email": "updated@example.com",
            "phone": "555-222-2222",
            "address": "222 New Street"
        }

        response = self.client.put(
            f"/customers/{customer_id}",
            json=update_data
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["first_name"], "Updated")
        self.assertEqual(data["last_name"], "Customer")
        self.assertEqual(data["email"], "updated@example.com")

    def test_delete_customer(self):
        with self.app.app_context():
            customer = Customer(
                first_name="Delete",
                last_name="Me",
                email="delete@example.com",
                phone="555-333-3333",
                address="333 Delete Street",
                password=bcrypt.generate_password_hash("testpassword").decode('utf-8')
            )

            db.session.add(customer)
            db.session.commit()

            customer_id = customer.id

        response = self.client.delete(
            f"/customers/{customer_id}"
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(
            data["message"],
            "Customer deleted successfully"
        )

    def test_login_customer(self):
        with self.app.app_context():
            customer = Customer(
                first_name="Login",
                last_name="Customer",
                email="login@example.com",
                phone="555-444-4444",
                address="444 Login Street",
                password=bcrypt.generate_password_hash("testpassword").decode('utf-8')
            )

            db.session.add(customer)
            db.session.commit()

        response = self.client.post(
            "/customers/login",
            json={
                "email": "login@example.com",
                "password": "testpassword"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIn("token", data)
        self.assertIsInstance(data["token"], str)

    def test_get_my_tickets(self):
        with self.app.app_context():
            customer = Customer(
                first_name="Ticket",
                last_name="Customer",
                email="ticket@example.com",
                phone="555-555-5555",
                address="555 Ticket Street",
                password=bcrypt.generate_password_hash("testpassword").decode('utf-8')
            )

            db.session.add(customer)
            db.session.commit()

            customer_id = customer.id

            ticket = ServiceTicket(
                customer_id=customer_id
            )

            db.session.add(ticket)
            db.session.commit()

        response = self.client.post(
            "/customers/login",
            json={
                "email": "ticket@example.com",
                "password": "testpassword"
            }
        )

        self.assertEqual(response.status_code, 200)

        token = response.get_json()["token"]

        response = self.client.get(
            "/customers/my-tickets",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["customer_id"], customer_id)

    def test_get_my_tickets_invalid_token(self):
        response = self.client.get(
            "/customers/my-tickets",
            headers={
                "Authorization": "Bearer invalidtoken"
            }
        )

        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()