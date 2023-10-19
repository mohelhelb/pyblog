import os


class Config:
    pass


class ConfigDevelopment(Config):
    # If the environment variable, PYBLOG_DEVELOPMENT_SECRET_KEY, exists and is not empty, assign SECRET_KEY to its value.
    # Otherwise, assign SECRET_KEY to "development".
    SECRET_KEY = os.environ.get("PYBLOG_DEVELOPMENT_SECRET_KEY") or "development"
    #
    SQLALCHEMY_DATABASE_URI = "sqlite:///pyblog.db"
    # UPLOAD_FOLDER = os.path.join(app.static_folder, "images") # Pending: Resolve circular import
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = "True"
    MAIL_USERNAME = os.environ.get("PYBLOG_MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("PYBLOG_MAIL_PASSWORD")
