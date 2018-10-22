"""Re-export API."""
from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='')

from boilerplateapp.api import auth  # noqa E402
from boilerplateapp.api import hello  # noqa E402
