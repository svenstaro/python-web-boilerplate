"""Simple wrapper around passlib that allows for lazy initilization."""
from passlib.context import CryptContext


class Passlib(object):
    """Passlib wrapper class that allows for lazy initilization.

    The part about the lazy initilization is important for using Flask with
    application factorties.
    """

    def __init__(self, app=None):
        """Construct a `Passlib` object. Optionally takes an `app`."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Lazy initializer which takes an `app` and sets up the internal context."""
        self.pwd_context = CryptContext(
            schemes=app.config['PASSLIB_SCHEMES'],
        )
