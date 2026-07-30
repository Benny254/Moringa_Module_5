"""
models.py
---------
SQLAlchemy models for the app: User and Note.

- User owns many Notes (one-to-many).
- Passwords are never stored in plain text — only a bcrypt hash is kept,
  and the hash is never serialized back to the client.
"""
from datetime import datetime

from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column("password_hash", db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    notes = db.relationship(
        "Note", back_populates="user", cascade="all, delete-orphan"
    )

    # --- password handling -------------------------------------------------
    @hybrid_property
    def password_hash(self):
        # Block reads of the raw hash from outside the class.
        raise AttributeError("password_hash is not a readable attribute")

    @password_hash.setter
    def password_hash(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self._password_hash = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def authenticate(self, password):
        """Return True if the given plaintext password matches the hash."""
        return bcrypt.check_password_hash(self._password_hash, password)

    # --- basic field validation --------------------------------------------
    @validates("username")
    def validate_username(self, key, username):
        if not username or not username.strip():
            raise ValueError("Username cannot be blank")
        return username.strip()

    @validates("email")
    def validate_email(self, key, email):
        if not email or "@" not in email:
            raise ValueError("A valid email is required")
        return email.strip().lower()

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="notes")

    @validates("title")
    def validate_title(self, key, title):
        if not title or not title.strip():
            raise ValueError("Title cannot be blank")
        return title.strip()

    @validates("content")
    def validate_content(self, key, content):
        if not content or not content.strip():
            raise ValueError("Content cannot be blank")
        return content.strip()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"