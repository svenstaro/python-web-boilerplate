"""Various testing utilities."""


def make_headers(user, method):
    """Return proper headers for the given `method` and `user`.

    Args:
        user - The `User` to generate the token for.
        method - The HTTP method. Possible values: "GET", "POST", "DELETE", "PUT"

    Returns:
        dict - Headers to use with the given `method` and containing a token for the given `user`.
    """
    token = user.generate_auth_token(salt='login')
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer {token}'.format(token=token.decode('ASCII')),
    }

    if method in ['POST', 'PUT']:
        headers['Content-Type'] = 'application/json',

    return headers
