from flask import jsonify, request
from . import inventory_bp
from app.models import Inventory
from app.extensions import db

from .schemas import InventorySchema


@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    inventory = Inventory.query.all()

    schema = InventorySchema()

    return schema.dump(inventory, many=True), 200

@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory_item(id):
    inventory = Inventory.query.get_or_404(id)

    schema = InventorySchema()

    return schema.dump(inventory), 200

@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory(id):
    inventory = Inventory.query.get_or_404(id)

    data = request.get_json()

    inventory.name = data.get('name', inventory.name)
    inventory.price = data.get('price', inventory.price)

    db.session.commit()

    schema = InventorySchema()

    return schema.dump(inventory), 200

@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    data = request.get_json()

    schema = InventorySchema()
    inventory = schema.load(data)

    db.session.add(inventory)
    db.session.commit()

    return schema.dump(inventory), 201

@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory(id):
    inventory = Inventory.query.get_or_404(id)

    db.session.delete(inventory)
    db.session.commit()

    return {'message': 'Inventory item deleted successfully'}, 200