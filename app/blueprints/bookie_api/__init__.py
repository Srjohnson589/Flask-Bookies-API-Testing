from flask import Blueprint

bookie_api = Blueprint('bookie_api', __name__, url_prefix='/bookie_api')

from . import routes