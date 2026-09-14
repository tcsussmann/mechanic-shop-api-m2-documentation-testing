from flask import jsonify, request
from . import mechanic_bp
from app.models import Mechanic
from app.extensions import db
from .schemas import MechanicSchema


@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    mechanics = Mechanic.query.all()

    mechanics.sort(
        key=lambda mechanic: len(mechanic.service_tickets),
        reverse=True
    )

    return jsonify([
        {
            'id': mechanic.id,
            'first_name': mechanic.first_name,
            'last_name': mechanic.last_name,
            'email': mechanic.email,
            'phone': mechanic.phone,
            'ticket_count': len(mechanic.service_tickets)
        }
        for mechanic in mechanics
    ])


@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()

    schema = MechanicSchema()
    mechanic = schema.load(data)

    db.session.add(mechanic)
    db.session.commit()

    return schema.dump(mechanic), 201

@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)

    data = request.get_json()

    mechanic.first_name = data.get('first_name', mechanic.first_name)
    mechanic.last_name = data.get('last_name', mechanic.last_name)
    mechanic.email = data.get('email', mechanic.email)
    mechanic.phone = data.get('phone', mechanic.phone)

    db.session.commit()

    schema = MechanicSchema()

    return schema.dump(mechanic), 200

@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)

    db.session.delete(mechanic)
    db.session.commit()

    return {'message': 'Mechanic deleted successfully'}, 200
