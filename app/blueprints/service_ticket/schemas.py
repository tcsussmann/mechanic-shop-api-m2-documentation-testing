from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

from app.models import ServiceTicket
from app.extensions import db
from app.blueprints.inventory.schemas import InventorySchema


class ServiceTicketSchema(SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)
    customer_id = fields.Integer(required=True)
    inventory = fields.Nested(InventorySchema, many=True, dump_only=True)

    class Meta:
        model = ServiceTicket
        load_instance = True
        sqla_session = db.session