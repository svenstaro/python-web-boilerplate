from flask import jsonify


def _prepare_response_data(message, data=None):
    output = {"message": message}
    if data:
        output["data"] = data

    return output


def ok(message="OK", data=None):
    response_data = _prepare_response_data(message, data)
    return jsonify(response_data), 200


def created(message="Created", data=None):
    response_data = _prepare_response_data(message, data)
    return jsonify(response_data), 201


def accepted(message="Accepted", data=None):
    response_data = _prepare_response_data(message, data)
    return jsonify(response_data), 202


def no_content(message="No Content", data=None):
    response_data = _prepare_response_data(message, data)
    return jsonify(response_data), 204


def bad_request(message="Bad Request", data=None):
    response_data = _prepare_response_data(message, data)
    return jsonify(response_data), 400


def unauthorized(message="Unauthorized"):
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 401


def forbidden(message="Forbidden"):
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 403


def not_found(message="Not Found"):
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 404


def method_not_allowed(message="Method Not Allowed"):
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 405


def conflict(message="Conflict"):
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 409


def unprocessable_entity(message="Unprocessable Entity"):
    response_data = _prepare_response_data(message)
    return jsonify(response_data), 422
