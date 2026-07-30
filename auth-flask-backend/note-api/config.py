"""
config.py
---------
Central place to configure the Flask app and initialize extensions.
Importing `app`, `db`, `bcrypt`, or `api` from here keeps every other
module (models, routes, seed script) working off the SAME instances,
which is required for Flask-SQLAlchemy / Flask-Migrate to work correctly.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from sqlalchemy import MetaData

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Naming convention keeps auto-generated migration constraint names consistent
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Secret key is required for signing the session cookie. In production this
# MUST come from an environment variable, never hard-coded.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# Session cookie settings — SameSite/secure settings matter once the
# frontend and backend live on different domains (e.g. Vercel + Render).
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = os.environ.get("FLASK_ENV") == "production"

db = SQLAlchemy(metadata=metadata)
db.init_app(app)

migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

api = Api(app)