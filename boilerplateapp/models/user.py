"""Module containing the `User` model."""
import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils.models import Timestamp

from flask import current_app

from boilerplateapp.extensions import db, passlib


class User(db.Model, Timestamp):
    """User model."""

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(120), nullable=False)
    current_auth_token = db.Column(db.String(36), index=True)
    last_action = db.Column(db.DateTime)

    def __init__(self, email, password):
        """Construct a `User`.

        Accepts an `email` and a `password`. The password is securely hashed
        before being written to the database.
        """
        self.email = email
        self.set_password(password)

    def __repr__(self):
        """Format a `User` object."""
        return '<User {email}>'.format(email=self.email)

    def set_password(self, new_password):
        """Hash a given `new_password` and write it into the `User.password_hash` attribute.

        It does not add this change to the session not commit the transaction!
        """
        self.password_hash = passlib.pwd_context.hash(new_password)

    def verify_password(self, candidate_password):
        """Verify a given `candidate_password` against the password hash stored in the `User`.

        Returns `True` if the password matches and `False` if it doesn't.
        """
        return passlib.pwd_context.verify(candidate_password, self.password_hash)

    def generate_auth_token(self):
        """Generate an auth token and save it to the `current_auth_token` column."""
        new_auth_token = uuid.uuid4()
        self.current_auth_token = '{auth_token}'.format(auth_token=new_auth_token)
        self.last_action = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        return new_auth_token

    @property
    def has_valid_auth_token(self):
        """Return whether or not the user has a valid auth token."""
        latest_valid_date = datetime.utcnow() - current_app.config['AUTH_TOKEN_TIMEOUT']
        return self.last_action and self.last_action > latest_valid_date

    @staticmethod
    def get_user_from_login_token(token):
        """Get a `User` from a login token.

        A login token has this format:
            <user uuid>:<auth token>
        """
        user_id, auth_token = token.split(':')
        user = db.session.query(User).filter_by(id=user_id, current_auth_token=auth_token).first()
        return user
