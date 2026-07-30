"""
app.py
------
Entry point for the Flask API. Registers all resources with Flask-RESTful.

Auth strategy: SERVER-SIDE SESSIONS.
  - On signup/login we store the user's id in the signed session cookie
    (`session['user_id']`). Flask signs this cookie with `app.secret_key`,
    so the client can't forge it, but it's still sent back on every request
    thanks to the browser's cookie jar (`credentials: 'include'` on fetch).
  - `check_session` lets the frontend ask "am I still logged in?" on page
    load/refresh.
  - `logout` clears the session server-side.

Route protection: every Note route calls `get_current_user()` first and
bails out with 401 if there's no valid session. Ownership is enforced by
filtering/looking up notes with `user_id == current_user.id`, so one user
can never see, edit, or delete another user's notes (returns 404, not 403,
to avoid leaking whether the note exists at all).
"""
from flask import request, session, make_response, jsonify
from flask_restful import Resource
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Note

# Allow the separate frontend dev server to send/receive the session cookie.
CORS(app, supports_credentials=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def get_current_user():
    """Return the logged-in User, or None if there's no valid session."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


def error(message, status):
    return make_response(jsonify({"error": message}), status)


# ---------------------------------------------------------------------------
# Auth resources
# ---------------------------------------------------------------------------
class Signup(Resource):
    """POST /signup -> create a new user and log them in immediately."""

    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return error("username, email, and password are required", 422)

        user = User(username=username, email=email)
        try:
            user.password_hash = password  # runs the length validation + hashing
            db.session.add(user)
            db.session.commit()
        except ValueError as ve:
            db.session.rollback()
            return error(str(ve), 422)
        except IntegrityError:
            db.session.rollback()
            return error("Username or email is already taken", 422)

        session["user_id"] = user.id
        return make_response(jsonify(user.to_dict()), 201)


class Login(Resource):
    """POST /login -> verify credentials and start a session."""

    def post(self):
        data = request.get_json() or {}
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter_by(username=username).first()
        if not user or not user.authenticate(password or ""):
            return error("Invalid username or password", 401)

        session["user_id"] = user.id
        return make_response(jsonify(user.to_dict()), 200)


class Logout(Resource):
    """DELETE /logout -> end the session."""

    def delete(self):
        session.pop("user_id", None)
        return make_response("", 204)


class CheckSession(Resource):
    """GET /check_session -> tell the frontend who (if anyone) is logged in."""

    def get(self):
        user = get_current_user()
        if not user:
            return error("Not authenticated", 401)
        return make_response(jsonify(user.to_dict()), 200)


# ---------------------------------------------------------------------------
# Note resources (protected, owner-scoped)
# ---------------------------------------------------------------------------
class NoteIndex(Resource):
    """GET /notes -> paginated list of the current user's notes.
    POST /notes -> create a new note for the current user."""

    def get(self):
        user = get_current_user()
        if not user:
            return error("Not authenticated", 401)

        try:
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 10))
        except ValueError:
            return error("page and per_page must be integers", 400)

        page = max(page, 1)
        per_page = min(max(per_page, 1), 100)  # clamp to a sane range

        pagination = Note.query.filter_by(user_id=user.id) \
            .order_by(Note.created_at.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)

        return make_response(jsonify({
            "notes": [note.to_dict() for note in pagination.items],
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        }), 200)

    def post(self):
        user = get_current_user()
        if not user:
            return error("Not authenticated", 401)

        data = request.get_json() or {}
        try:
            note = Note(
                title=data.get("title"),
                content=data.get("content"),
                user_id=user.id,
            )
            db.session.add(note)
            db.session.commit()
        except ValueError as ve:
            db.session.rollback()
            return error(str(ve), 422)

        return make_response(jsonify(note.to_dict()), 201)


class NoteDetail(Resource):
    """GET/PATCH/DELETE /notes/<id> -> only works on notes owned by the
    current user. Notes owned by someone else 404 (not 403) so we don't
    reveal whether the id exists at all."""

    def _get_owned_note_or_none(self, user, note_id):
        return Note.query.filter_by(id=note_id, user_id=user.id).first()

    def get(self, id):
        user = get_current_user()
        if not user:
            return error("Not authenticated", 401)
        note = self._get_owned_note_or_none(user, id)
        if not note:
            return error("Note not found", 404)
        return make_response(jsonify(note.to_dict()), 200)

    def patch(self, id):
        user = get_current_user()
        if not user:
            return error("Not authenticated", 401)
        note = self._get_owned_note_or_none(user, id)
        if not note:
            return error("Note not found", 404)

        data = request.get_json() or {}
        try:
            if "title" in data:
                note.title = data["title"]
            if "content" in data:
                note.content = data["content"]
            db.session.commit()
        except ValueError as ve:
            db.session.rollback()
            return error(str(ve), 422)

        return make_response(jsonify(note.to_dict()), 200)

    def delete(self, id):
        user = get_current_user()
        if not user:
            return error("Not authenticated", 401)
        note = self._get_owned_note_or_none(user, id)
        if not note:
            return error("Note not found", 404)

        db.session.delete(note)
        db.session.commit()
        return make_response("", 204)


# ---------------------------------------------------------------------------
# Route registration
# ---------------------------------------------------------------------------
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CheckSession, "/check_session")
api.add_resource(NoteIndex, "/notes")
api.add_resource(NoteDetail, "/notes/<int:id>")


@app.route("/")
def index():
    return {"message": "Notes API is running"}


if __name__ == "__main__":
    app.run(port=5555, debug=True)