import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    # SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{os.environ.get('POSTGRES_PASSWORD')}@localhost:55003/info253"

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

    API_TITLE = "My API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"