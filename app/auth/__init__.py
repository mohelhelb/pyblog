
from flask import Blueprint

bp_auth = Blueprint("bp_auth", __name__, template_folder="templates")

from app.auth import views
