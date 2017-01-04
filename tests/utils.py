"""Various testing utilities."""


def make_headers(method, user=None):
    """Return proper headers for the given `method` and `user`.

    Args:
        method - The HTTP method. Possible values: "GET", "POST", "DELETE", "PUT"
        user - The `User` to generate the token for.

    Returns:
        dict - Headers to use with the given `method` and containing a token for the given `user`.
    """
    headers = {
        'Accept': 'application/json',
    }

    if user:
        token = user.generate_auth_token(salt='login')
        headers['Authorization'] = 'Bearer {token}'.format(token=token.decode('ASCII'))

    if method in ['POST', 'PUT']:
        headers['Content-Type'] = 'application/json',

    return headers
