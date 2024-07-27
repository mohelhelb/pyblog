
from flask import Blueprint

bp_post = Blueprint("bp_post", __name__, template_folder="templates")

from pyblog.post import views
