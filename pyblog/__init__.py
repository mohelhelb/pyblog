from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from pyblog.config import ConfigDevelopment

app = Flask(__name__)

app.config.from_object(ConfigDevelopment)  # Configuration 

# Extensions >

db = SQLAlchemy(app)  # Flask: SQLAlchemy

bcrypt = Bcrypt(app)  # Flask: Bcrypt 

mail = Mail(app)  # Flask: Mail

# Flask: Login >
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.refresh_view = "login"
login_manager.needs_refresh_message_category = "info"
# < Flask: Login

# < Extensions

import pyblog.views  







