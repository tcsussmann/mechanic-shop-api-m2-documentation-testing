import bcrypt
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from .extensions import db, ma, limiter, cache, jwt, bcrypt
from .blueprints.customer import customer_bp
from .blueprints.mechanic import mechanic_bp
from .blueprints.service_ticket import service_ticket_bp
from .blueprints.inventory import inventory_bp


def create_app(config_name):
    app = Flask(__name__)

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.yaml'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Mechanic Shop API'
        }
    )

    app.register_blueprint(
        swaggerui_blueprint,
        url_prefix=SWAGGER_URL
    )

    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(
        service_ticket_bp,
        url_prefix='/service-tickets'
    )
    app.register_blueprint(
        inventory_bp,
        url_prefix='/inventory'
    )

    return app