"""Module containing all handlers for the API."""
from flask import g, request
from datetime import datetime

from boilerplateapp.extensions import db
from boilerplateapp.models.user import User
from boilerplateapp.responses import (
    bad_request,
    unauthorized,
    forbidden,
    not_found,
    method_not_allowed,
    conflict,
    unprocessable_entity,
)


def register_handlers(app):
    """Helper function for which is called from the application factory."""
    @app.before_request
    def require_json_input():
        """Require JSON input.

        If the request's method is either 'POST' or 'PUT', require the
        'Content-Type' to be JSON.
        """
        if request.method in ['POST', 'PUT']:
            if request.headers['Content-Type'] != 'application/json':
                return bad_request("'Content-Type' must be 'application/json'.")

    @app.before_request
    def default_login_required():
        # If this is an error or something else without a proper endpoint, just
        # return straight away.
        if not request.endpoint:
            return

        view = app.view_functions[request.endpoint]

        if getattr(view, 'login_exempt', False):
            return

        token_header = request.headers.get('Authorization')
        if not token_header:
            return unauthorized("'Authorization' not found in headers.")

        if 'Bearer ' not in token_header:
            return unauthorized("'Authorization' header has wrong format.")

        token = token_header.replace('Bearer ', '')
        user = User.get_user_from_login_token(token)

        if not user:
            return unauthorized("Invalid login token.")

        # Require user to re-login if the last action is too long ago.
        if not user.has_valid_auth_token:
            return unauthorized("Auth token too old, please log in again.")

        # At this point the user is considered successfully authenticated.
        user.last_action = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        g.current_user = user

    @app.after_request
    def add_cors_headers(response):
        """Add CORS to the headers of this request."""
        response.headers['Access-Control-Allow-Origin'] = app.config['CORS_ALLOW_ORIGIN']
        response.headers['Access-Control-Allow-Methods'] = app.config['CORS_ALLOW_METHODS']
        response.headers['Access-Control-Allow-Headers'] = app.config['CORS_ALLOW_HEADERS']
        return response

    @app.errorhandler(400)
    def handle_bad_request(e):
        return bad_request(e.name)

    @app.errorhandler(401)
    def handle_unauthorized(e):
        return unauthorized(e.name)

    @app.errorhandler(403)
    def handle_forbidden(e):
        return forbidden(e.name)

    @app.errorhandler(404)
    def handle_not_found(e):
        return not_found(e.name)

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return method_not_allowed(e.name)

    @app.errorhandler(409)
    def handle_conflict(e):
        return conflict(e.name)

    @app.errorhandler(422)
    def handle_unprocessable_entity(e):
        # webargs attaches additional metadata to the `data` attribute
        data = getattr(e, 'data') if hasattr(e, 'data') else None
        if data:
            # Get validations from the ValidationError object
            messages = data['messages']
        else:
            messages = ['Invalid request']
        return unprocessable_entity(messages)
