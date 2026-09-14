from flask import jsonify, request
from . import service_ticket_bp
from app.models import ServiceTicket, Mechanic, Inventory
from app.extensions import db
from .schemas import ServiceTicketSchema


@service_ticket_bp.route('/', methods=['POST'])
def create_service_ticket():
    data = request.get_json()

    schema = ServiceTicketSchema()
    service_ticket = schema.load(data)

    db.session.add(service_ticket)
    db.session.commit()

    return schema.dump(service_ticket), 201


@service_ticket_bp.route('/', methods=['GET'])
def get_service_tickets():
    service_tickets = ServiceTicket.query.all()

    schema = ServiceTicketSchema()

    return schema.dump(service_tickets, many=True), 200

@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    service_ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    service_ticket.mechanics.append(mechanic)

    db.session.commit()

    schema = ServiceTicketSchema()

    return schema.dump(service_ticket), 200

@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    service_ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    service_ticket.mechanics.remove(mechanic)

    db.session.commit()

    schema = ServiceTicketSchema()

    return schema.dump(service_ticket), 200

@service_ticket_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    service_ticket = ServiceTicket.query.get_or_404(ticket_id)

    data = request.get_json()

    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])

    for mechanic_id in add_ids:
        mechanic = Mechanic.query.get_or_404(mechanic_id)
        if mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)

    for mechanic_id in remove_ids:
        mechanic = Mechanic.query.get_or_404(mechanic_id)
        if mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)

    db.session.commit()

    schema = ServiceTicketSchema()

    return schema.dump(service_ticket), 200

@service_ticket_bp.route('/<int:ticket_id>/add-inventory/<int:inventory_id>', methods=['PUT'])
def add_inventory(ticket_id, inventory_id):
    service_ticket = ServiceTicket.query.get_or_404(ticket_id)
    inventory = Inventory.query.get_or_404(inventory_id)

    if inventory not in service_ticket.inventory:
        service_ticket.inventory.append(inventory)

    db.session.commit()

    schema = ServiceTicketSchema()

    return schema.dump(service_ticket), 200