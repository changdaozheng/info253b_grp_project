import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "My API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

    API_TITLE = "My API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"