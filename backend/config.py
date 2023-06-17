"""the purpose of this file is to easily
switch between our various development states"""
import os
from dotenv import load_dotenv

load_dotenv()

# BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATION = False

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_TEST_DATABASE_URI")
    TESTING = True
    SQLALCHEMY_ECHO = False

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_PROD_DATABASE_URI")
    DEBUG = False
    SQLALCHEMY_ECHO = False
