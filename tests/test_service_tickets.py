from app import create_app
from app.extensions import db
from app.models import ServiceTicket, Customer, Mechanic, Inventory
import unittest

class TestServiceTicket(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

#           First route: POST /service-tickets/

    def test_create_service_ticket(self):
        with self.app.app_context():
            customer = Customer(
                first_name="Test",
                last_name="Customer",
                email="ticketcustomer@example.com",
                phone="555-555-5555",
                address="123 Test Street",
                password="testpassword"
            )

            db.session.add(customer)
            db.session.commit()

            customer_id = customer.id

        ticket_data = {
            "customer_id": customer_id
        }

        response = self.client.post(
            "/service-tickets/",
            json=ticket_data
        )

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data["customer_id"], customer_id)

#           Second route: GET /service-tickets/

    def test_get_service_tickets(self):
        with self.app.app_context():
            customer = Customer(
                first_name="Test",
                last_name="Customer",
                email="getticket@example.com",
                phone="555-555-5555",
                address="123 Test Street",
                password="testpassword"
            )

            db.session.add(customer)
            db.session.commit()

            customer_id = customer.id

            ticket = ServiceTicket(
                customer_id=customer_id
            )

            db.session.add(ticket)
            db.session.commit()

        response = self.client.get("/service-tickets/")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["customer_id"], customer_id)

#           Third route: PUT /service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>

    def test_assign_mechanic(self):
        with self.app.app_context():
            customer = Customer(
                first_name="Test",
                last_name="Customer",
                email="assignmechanic@example.com",
                phone="555-555-5555",
                address="123 Test Street",
                password="testpassword"
            )

            mechanic = Mechanic(
                first_name="Test",
                last_name="Mechanic",
                email="mechanic@example.com",
                phone="555-555-5555"
            )

            db.session.add_all([customer, mechanic])
            db.session.commit()

            customer_id = customer.id
            mechanic_id = mechanic.id

            ticket = ServiceTicket(
                customer_id=customer_id
            )

            db.session.add(ticket)
            db.session.commit()

            ticket_id = ticket.id

        response = self.client.put(
            f"/service-tickets/{ticket_id}/assign-mechanic/{mechanic_id}"
        )

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["id"], ticket_id)
        self.assertEqual(data["customer_id"], customer_id)

#           Fourth route: PUT /service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>

    def test_remove_mechanic(self):
        with self.app.app_context():
            customer = Customer(
                first_name="Test",
                last_name="Customer",
                email="removemechanic@example.com",
                phone="555-555-5555",
                address="123 Test Street",
                password="testpassword"
            )

            mechanic = Mechanic(
                first_name="Test",
                last_name="Mechanic",
                email="remove@example.com",
                phone="555-555-5555"
            )

            db.session.add_all([customer, mechanic])
            db.session.commit()

            customer_id = customer.id
            mechanic_id = mechanic.id

            ticket = ServiceTicket(
                customer_id=customer_id
            )

            ticket.mechanics.append(mechanic)

            db.session.add(ticket)
            db.session.commit()

            ticket_id = ticket.id

        response = self.client.put(
            f"/service-tickets/{ticket_id}/remove-mechanic/{mechanic_id}"
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            ticket = ServiceTicket.query.get(ticket_id)

            self.assertEqual(len(ticket.mechanics), 0)

#           Fifth route: PUT /service-tickets/<ticket_id>/edit

    def test_edit_ticket_mechanics(self):
        with self.app.app_context():
            customer = Customer(
                first_name="Test",
                last_name="Customer",
                email="editticket@example.com",
                phone="555-555-5555",
                address="123 Test Street",
                password="testpassword"
            )

            mechanic1 = Mechanic(
                first_name="First",
                last_name="Mechanic",
                email="first@example.com",
                phone="555-555-5555"
            )

            mechanic2 = Mechanic(
                first_name="Second",
                last_name="Mechanic",
                email="second@example.com",
                phone="555-555-5555"
            )

            db.session.add_all([customer, mechanic1, mechanic2])
            db.session.commit()

            customer_id = customer.id
            mechanic1_id = mechanic1.id
            mechanic2_id = mechanic2.id

            ticket = ServiceTicket(
                customer_id=customer_id
            )

            ticket.mechanics.append(mechanic1)

            db.session.add(ticket)
            db.session.commit()

            ticket_id = ticket.id

        response = self.client.put(
            f"/service-tickets/{ticket_id}/edit",
            json={
                "add_ids": [mechanic2_id],
                "remove_ids": [mechanic1_id]
            }
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            ticket = ServiceTicket.query.get(ticket_id)

            self.assertEqual(len(ticket.mechanics), 1)
            self.assertEqual(ticket.mechanics[0].id, mechanic2_id)

#           Sixth route: PUT /service-tickets/<ticket_id>/add-inventory/<inventory_id>

    def test_add_inventory(self):
        with self.app.app_context():
            customer = Customer(
                first_name="Test",
                last_name="Customer",
                email="addinventory@example.com",
                phone="555-555-5555",
                address="123 Test Street",
                password="testpassword"
            )

            inventory = Inventory(
                name="Test Oil Filter",
                price=19.99
            )

            db.session.add_all([customer, inventory])
            db.session.commit()

            customer_id = customer.id
            inventory_id = inventory.id

            ticket = ServiceTicket(
                customer_id=customer_id
            )

            db.session.add(ticket)
            db.session.commit()

            ticket_id = ticket.id

        response = self.client.put(
            f"/service-tickets/{ticket_id}/add-inventory/{inventory_id}"
        )

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            ticket = ServiceTicket.query.get(ticket_id)

            self.assertEqual(len(ticket.inventory), 1)
            self.assertEqual(ticket.inventory[0].id, inventory_id)