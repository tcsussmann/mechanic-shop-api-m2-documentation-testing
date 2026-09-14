from flask import jsonify, request
from datetime import datetime
from . import customer_bp
from app.models import Customer
from app.extensions import db, limiter, cache, bcrypt
from .schemas import CustomerSchema, login_schema
from app.utils.util import encode_token, token_required


@customer_bp.route('/', methods=['GET'])
@limiter.limit("5 per minute")
@cache.cached(timeout=60, query_string=True)
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 2, type=int)

    customers = Customer.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        'generated_at': datetime.now().isoformat(),
        'customers': [
            {
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'phone': customer.phone,
                'address': customer.address
            }
            for customer in customers.items
        ],
        'page': customers.page,
        'per_page': customers.per_page,
        'total': customers.total,
        'pages': customers.pages
    })


@customer_bp.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()

    schema = CustomerSchema()
    customer = schema.load(data)

    db.session.add(customer)
    db.session.commit()

    return schema.dump(customer), 201

@customer_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)

    data = request.get_json()

    customer.first_name = data.get('first_name', customer.first_name)
    customer.last_name = data.get('last_name', customer.last_name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    customer.address = data.get('address', customer.address)

    db.session.commit()

    schema = CustomerSchema()

    return schema.dump(customer), 200

@customer_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)

    db.session.delete(customer)
    db.session.commit()

    return {'message': 'Customer deleted successfully'}, 200

@customer_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    customer = Customer.query.filter_by(
        email=data['email']
    ).first()

    if customer and bcrypt.check_password_hash(
        customer.password,
        data['password']
    ):
        token = encode_token(customer.id)
        return {'token': token}, 200

    return {'message': 'Invalid credentials'}, 401

@customer_bp.route('/my-tickets', methods=['GET'])
@token_required
def my_tickets(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    return jsonify([
        {
            'id': ticket.id,
            'customer_id': ticket.customer_id
        }
        for ticket in customer.service_tickets
    ])