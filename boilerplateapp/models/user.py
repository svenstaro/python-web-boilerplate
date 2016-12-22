from itsdangerous import JSONWebSignatureSerializer, BadSignature
from flask import current_app
from sqlalchemy_utils.models import Timestamp

from boilerplateapp.extensions import db, passlib


class User(db.Model, Timestamp):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, new_password):
        self.password_hash = passlib.pwd_context.hash(new_password)

    def verify_password(self, candidate_password) -> bool:
        return passlib.pwd_context.verify(candidate_password, self.password_hash)

    def generate_auth_token(self, salt):
        serializer = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'], salt)
        return serializer.dumps({'id': self.id})

    @staticmethod
    def get_user_from_auth_token(token, salt):
        serializer = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'], salt)
        try:
            data = serializer.loads(token)
        except BadSignature:
            return False

        user = db.session.query(User).get(data['id'])
        return user
