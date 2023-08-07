from flask import Flask
from flask_bcrypt import Bcrypt
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


import pyblog.views  







