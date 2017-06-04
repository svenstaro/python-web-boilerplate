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
        user_id = user.id
        auth_token = user.generate_auth_token()
        login_token = '{user_id}:{auth_token}'.format(
            user_id=user_id,
            auth_token=auth_token,
        )
        headers['Authorization'] = 'Bearer {login_token}'.format(login_token=login_token)

    if method in ['POST', 'PUT']:
        headers['Content-Type'] = 'application/json',

    return headers
