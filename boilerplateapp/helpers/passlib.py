from passlib.context import CryptContext


class Passlib(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.pwd_context = CryptContext(
            schemes=app.config['PASSLIB_SCHEMES']
        )
