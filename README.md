# Mechanic Shop API

A RESTful API for managing customers, mechanics, inventory, and service tickets for a mechanic shop.

## Technologies

* Python
* Flask
* SQLAlchemy
* MySQL
* Marshmallow
* Flask-Marshmallow
* Flask-Limiter
* Flask-Caching
* Flask-JWT-Extended
* Flask-Bcrypt
* Flask-Swagger
* Flask-Swagger-UI
* unittest

## Project Structure

```text
mechanic-shop-api/
├── app/
│   ├── blueprints/
│   │   ├── customer/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── mechanic/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── inventory/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   └── service_ticket/
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       └── schemas.py
│   ├── static/
│   │   └── swagger.yaml
│   ├── __init__.py
│   ├── extensions.py
│   └── models.py
├── tests/
│   ├── __init__.py
│   ├── test_customers.py
│   ├── test_mechanics.py
│   ├── test_inventory.py
│   └── test_service_tickets.py
├── app.py
├── config.py
├── requirements.txt
├── .env
└── .gitignore
```

## Database

The application uses MySQL and SQLAlchemy.

The development database is named:

```text
mechanic_shop
```

The test suite uses a separate database:

```text
mechanic_shop_test
```

The database connection uses environment variables for sensitive configuration.

Create a `.env` file in the project root:

```text
MYSQL_PASSWORD=your_mysql_password
JWT_SECRET_KEY=your_jwt_secret_key
```

The `.env` file is included in `.gitignore` and should not be committed to GitHub.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/tcsussmann/mechanic-shop-api-m2-documentation-testing.git
cd mechanic-shop-api-m2-documentation-testing
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Install all required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure the environment variables

Create a `.env` file in the project root:

```text
MYSQL_PASSWORD=your_mysql_password
JWT_SECRET_KEY=your_jwt_secret_key
```

Replace the placeholder values with your local MySQL password and JWT secret.

### 5. Create the MySQL databases

Create the development database:

```text
mechanic_shop
```

Create the testing database:

```text
mechanic_shop_test
```

### 6. Run the Flask application

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

## API Documentation

This project includes interactive API documentation using Flask-Swagger-UI.

After starting the Flask application, open:

```text
http://127.0.0.1:5000/api/docs/
```

The Swagger UI provides documentation for the API routes, including request methods, parameters, responses, and authentication information.

The OpenAPI specification is located at:

```text
app/static/swagger.yaml
```

## Authentication

Customer login uses token-based authentication.

The login endpoint is:

```text
POST /customers/login
```

A successful login returns a JWT access token.

The following endpoint requires a valid JWT:

```text
GET /customers/my-tickets
```

When using the protected endpoint, include the token in the `Authorization` header:

```text
Authorization: Bearer <your_token>
```

## API Endpoints

### Customers

| Method | Endpoint                | Description                                      |
| ------ | ----------------------- | ------------------------------------------------ |
| GET    | `/customers/`           | Get customers with pagination                    |
| POST   | `/customers/`           | Create a customer                                |
| PUT    | `/customers/<id>`       | Update a customer                                |
| DELETE | `/customers/<id>`       | Delete a customer                                |
| POST   | `/customers/login`      | Authenticate a customer                          |
| GET    | `/customers/my-tickets` | Get the authenticated customer's service tickets |

### Mechanics

| Method | Endpoint          | Description       |
| ------ | ----------------- | ----------------- |
| GET    | `/mechanics/`     | Get all mechanics |
| POST   | `/mechanics/`     | Create a mechanic |
| PUT    | `/mechanics/<id>` | Update a mechanic |
| DELETE | `/mechanics/<id>` | Delete a mechanic |

### Inventory

| Method | Endpoint          | Description              |
| ------ | ----------------- | ------------------------ |
| GET    | `/inventory/`     | Get all inventory        |
| GET    | `/inventory/<id>` | Get an inventory item    |
| POST   | `/inventory/`     | Create an inventory item |
| PUT    | `/inventory/<id>` | Update an inventory item |
| DELETE | `/inventory/<id>` | Delete an inventory item |

### Service Tickets

| Method | Endpoint                                                     | Description                                   |
| ------ | ------------------------------------------------------------ | --------------------------------------------- |
| POST   | `/service-tickets/`                                          | Create a service ticket                       |
| GET    | `/service-tickets/`                                          | Get all service tickets                       |
| PUT    | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a service ticket         |
| PUT    | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a service ticket       |
| PUT    | `/service-tickets/<ticket_id>/edit`                          | Add or remove mechanics from a service ticket |
| PUT    | `/service-tickets/<ticket_id>/add-inventory/<inventory_id>`  | Add inventory to a service ticket             |

## Relationships

The API uses the following database relationships:

* A one-to-many relationship between customers and service tickets.
* A many-to-many relationship between service tickets and mechanics.
* A many-to-many relationship between service tickets and inventory.

The many-to-many relationships use association tables to connect the related records.

## Testing

The project uses Python's built-in `unittest` framework.

There is a separate test file for each blueprint:

* `tests/test_customers.py`
* `tests/test_mechanics.py`
* `tests/test_inventory.py`
* `tests/test_service_tickets.py`

The test suite includes tests for all 21 API routes as well as a negative authentication test.

Run the complete test suite from the project root:

```bash
python -m unittest discover tests
```

A successful test run should report:

```text
Ran 22 tests

OK
```

## Running the API

After starting the Flask server:

```bash
python app.py
```

API requests can be made using Swagger UI, Postman, or another API client.

Example:

```text
GET http://127.0.0.1:5000/service-tickets/
```
