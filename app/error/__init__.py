
from flask import Blueprint

bp_error = Blueprint("bp_error", __name__, template_folder="templates")

from app.error import views
