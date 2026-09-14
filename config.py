import os
from dotenv import load_dotenv

load_dotenv()


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://root:{os.getenv('MYSQL_PASSWORD')}"
        "@localhost/mechanic_shop"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    CACHE_TYPE = "SimpleCache"