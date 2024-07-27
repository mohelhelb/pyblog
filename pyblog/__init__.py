
### IMPORTS  ###################################################################  

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


### EXTENSIONS #################################################################

# Flask-SQLAlchemy
db = SQLAlchemy()

# Flask-Bcrypt
bcrypt = Bcrypt()

# Flask-mail
mail = Mail()

# Flask-login
login_manager = LoginManager()
login_manager.login_view = "bp_auth.login"
login_manager.login_message_category = "info"
login_manager.refresh_view = "bp_auth.login"
login_manager.needs_refresh_message_category = "info"

def create_app(ConfigClass=None):
    # Create and configure the application:
    app = Flask(__name__)  
    app.config.from_object(ConfigClass)

    # Bind extensions to the application:
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Register blueprints: 
    from pyblog.auth import bp_auth
    from pyblog.main import bp_main
    from pyblog.post import bp_post
    from pyblog.user import bp_user 
    from pyblog.error import bp_error 
                                  
    app.register_blueprint(bp_auth) 
    app.register_blueprint(bp_main) 
    app.register_blueprint(bp_post) 
    app.register_blueprint(bp_user) 
    app.register_blueprint(bp_error)

    return app








