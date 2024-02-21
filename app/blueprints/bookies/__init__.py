from flask import Blueprint

bookies = Blueprint('bookies', __name__, template_folder='bookies_templates')

from . import routes