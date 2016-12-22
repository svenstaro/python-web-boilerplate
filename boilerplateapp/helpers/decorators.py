import functools


def login_exempt(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    decorated_function.login_exempt = True
    return decorated_function
