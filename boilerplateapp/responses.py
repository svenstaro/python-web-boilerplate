"""Module containing all possible responses for this API."""
from flask import jsonify


def _prepare_response_data(message, data=None):
    """Helper method to prepare response output.

    Returns a simple dict containing a key `message` and optionally a key `data`.
    """
    output = {"message": message}
    if data:
        output["data"] = data

    return output


def ok(message="OK", data=None):
    """Response for HTTP `OK`."""
    response_data = _prepare_response_data(message, data)
    return jsonify(response_data), 200


def created(message="Created", data=None):
    """Response for HTTP `CREATED`."""
    response_data = _prepare_response_data(message, data)
    return jsonify(response_data), 201


def accepted(message="Accepted", data=None):
    """Response for HTTP `ACCEPTED`."""
    response_data = _prepare_response_data(message, data)
    return jsonify(response_data), 202


def no_content(message="No Content"):
    """Response for HTTP `NO CONTENT`."""
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 204


def bad_request(message="Bad Request", data=None):
    """Response for HTTP `BAD REQUEST`."""
    response_data = _prepare_response_data(message, data)
    return jsonify(response_data), 400


def unauthorized(message="Unauthorized"):
    """Response for HTTP `UNAUTHORIZED`."""
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 401


def forbidden(message="Forbidden"):
    """Response for HTTP `FORBIDDEN`."""
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 403


def not_found(message="Not Found"):
    """Response for HTTP `NOT FOUND`."""
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 404


def method_not_allowed(message="Method Not Allowed"):
    """Response for HTTP `METHOD NOT ALLOWED`."""
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 405


def conflict(message="Conflict"):
    """Response for HTTP `CONFLICT`."""
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 409


def unprocessable_entity(message="Unprocessable Entity"):
    """Response for HTTP `UNPROCESSABLE ENTITY`."""
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 422
