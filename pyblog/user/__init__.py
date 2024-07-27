
from flask import Blueprint

bp_user = Blueprint("bp_user", __name__, template_folder="templates")

from pyblog.user import views
