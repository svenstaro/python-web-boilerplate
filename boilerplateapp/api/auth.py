from webargs.flaskparser import use_args

from boilerplateapp.api import api
from boilerplateapp.extensions import db
from boilerplateapp.models.user import User
from boilerplateapp.schemas.user import UserSchema
from boilerplateapp.helpers.decorators import login_exempt
from boilerplateapp.responses import ok, conflict, created, unauthorized


@api.route('/login', methods=['POST'])
@login_exempt
@use_args(UserSchema())
def login(args):
    user = db.session.query(User).filter_by(email=args['email']).first()

    # For privacy reasons, we'll not provide the exact reason for failure here.
    if not user:
        return unauthorized("Username or password incorrect.")
    if not user.verify_password(args['password']):
        return unauthorized("Username or password incorrect.")

    token = user.generate_auth_token(salt='login')

    return ok(data=token.decode('ASCII'))


@api.route('/register', methods=['POST'])
@login_exempt
@use_args(UserSchema())
def register(args):
    if db.session.query(User).filter_by(email=args['email']).first():
        return conflict("User already exists.")

    new_user = User(args['email'], args['password'])
    db.session.add(new_user)
    db.session.commit()

    user_schema = UserSchema()

    return created(data=user_schema.dump(new_user).data)
