
from flask import Blueprint

bp_main = Blueprint("bp_main", __name__, template_folder="templates")

from pyblog.main import views