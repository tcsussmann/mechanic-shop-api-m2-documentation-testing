from functools import wraps

from flask import request
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_identity


def encode_token(customer_id):
    return create_access_token(identity=str(customer_id))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        customer_id = get_jwt_identity()
        return f(customer_id, *args, **kwargs)

    return decorated