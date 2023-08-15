from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from pyblog.config import ConfigDevelopment

app = Flask(__name__)

# Configuration
app.config.from_object(ConfigDevelopment) 

# Extensions

## Flask: SQLAlchemy
db = SQLAlchemy(app) 

## Flask: Bcrypt
bcrypt = Bcrypt(app) 

## Flask: Login
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.refresh_view = "login"
login_manager.needs_refresh_message_category = "info"

import pyblog.views  







