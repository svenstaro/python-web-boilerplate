"""Contains a bunch of helpful decorators."""
import functools


def login_exempt(f):
    """All routes decorated with this will be exempt from authorization.

    This means that using this decorator a function can be marked for anonymous access.

    Example:

        @api.route('/login', methods=['POST'])
        @login_exempt
        def login():
            pass
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    decorated_function.login_exempt = True
    return decorated_function
