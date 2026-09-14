# Mechanic Shop API

A RESTful API for managing customers, mechanics, and service tickets for a mechanic shop.

## Technologies

* Python
* Flask
* SQLAlchemy
* MySQL
* Marshmallow
* Flask-Marshmallow
* Postman

## Project Structure

```text
2026-08-28_mechanic_shop_api/
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
│   │   └── service_ticket/
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       └── schemas.py
│   ├── __init__.py
│   ├── extensions.py
│   └── models.py
├── app.py
├── config.py
├── .env
└── .gitignore
```

## Database

This project uses a MySQL database named `mechanic_shop`.

The application uses SQLAlchemy to interact with the database and Marshmallow for serialization and deserialization.

The database connection uses an environment variable for the MySQL password:

```text
MYSQL_PASSWORD=your_mysql_password
```

The `.env` file is included in `.gitignore` and should not be committed to GitHub.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/tcsussmann/mechanic-shop-api.git
cd mechanic-shop-api
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Install the required packages:

```bash
pip install flask flask-sqlalchemy flask-marshmallow marshmallow marshmallow-sqlalchemy mysql-connector-python python-dotenv
```

### 4. Configure the environment variable

Create a `.env` file in the project root:

```text
MYSQL_PASSWORD=your_mysql_password
```

Replace `your_mysql_password` with your MySQL password.

### 5. Create the MySQL database

Create a MySQL database named:

```text
mechanic_shop
```

### 6. Run the Flask application

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Customers

| Method | Endpoint          | Description       |
| ------ | ----------------- | ----------------- |
| GET    | `/customers/`     | Get all customers |
| POST   | `/customers/`     | Create a customer |
| PUT    | `/customers/<id>` | Update a customer |
| DELETE | `/customers/<id>` | Delete a customer |

### Mechanics

| Method | Endpoint          | Description       |
| ------ | ----------------- | ----------------- |
| GET    | `/mechanics/`     | Get all mechanics |
| POST   | `/mechanics/`     | Create a mechanic |
| PUT    | `/mechanics/<id>` | Update a mechanic |
| DELETE | `/mechanics/<id>` | Delete a mechanic |

### Service Tickets

| Method | Endpoint                                                     | Description                             |
| ------ | ------------------------------------------------------------ | --------------------------------------- |
| GET    | `/service-tickets/`                                          | Get all service tickets                 |
| POST   | `/service-tickets/`                                          | Create a service ticket                 |
| PUT    | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Assign a mechanic to a service ticket   |
| PUT    | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove a mechanic from a service ticket |

## Relationships

The API uses:

* A one-to-many relationship between customers and service tickets.
* A many-to-many relationship between service tickets and mechanics.

The many-to-many relationship uses the `service_ticket_mechanic` association table.

## Testing

The API endpoints were tested using Postman.

GET requests do not require a request body.

POST requests use JSON request bodies containing the appropriate fields.

The service ticket assign/remove mechanic endpoints use PUT requests and do not require a request body.

## Running the API

After starting the Flask server, API requests can be made using Postman or another API client.

Example:

```text
GET http://127.0.0.1:5000/service-tickets/
```
