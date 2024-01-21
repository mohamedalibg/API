import secrets

import app

SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = secrets.token_hex(16)

print(f"SQLALCHEMY_DATABASE_URI: {SQLALCHEMY_DATABASE_URI}")
print(f"SQLALCHEMY_TRACK_MODIFICATIONS: {SQLALCHEMY_TRACK_MODIFICATIONS}")
print(f"SECRET_KEY: {SECRET_KEY}")
# Inside __init__.py or your configuration file

