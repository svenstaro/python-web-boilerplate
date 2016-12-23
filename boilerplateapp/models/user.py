"""Module containing the `User` model."""
from itsdangerous import JSONWebSignatureSerializer, BadSignature
from flask import current_app
from sqlalchemy_utils.models import Timestamp

from boilerplateapp.extensions import db, passlib


class User(db.Model, Timestamp):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(120), nullable=False)

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

    def generate_auth_token(self, salt):
        """Generate a token containing the `id` of the current user with a given `salt`.

        It should be noted that the `salt` is a namespace rather than
        cryptographic salt so it doesn't need to be secure.
        """
        serializer = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'], salt)
        return serializer.dumps({'id': self.id})

    @staticmethod
    def get_user_from_auth_token(token, salt):
        """Get a `User` from a token with `salt`.

        It should be noted that the `salt` is a namespace rather than
        cryptographic salt so it doesn't need to be secure.
        The `salt` needs to be match the `salt` value this token was generated with.
        """
        serializer = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'], salt)
        try:
            data = serializer.loads(token)
        except BadSignature:
            return False

        user = db.session.query(User).get(data['id'])
        return user
