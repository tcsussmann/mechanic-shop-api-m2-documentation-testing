from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import Customer
from app.extensions import db

ma = Marshmallow()


class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session

login_schema = CustomerSchema(
    only=('email', 'password')
)