import os


class Config:
    pass


class ConfigDevelopment(Config):
    SECRET_KEY = os.environ.get("PYBLOG_SECRET_KEY") or "development"
    SQLALCHEMY_DATABASE_URI = "sqlite:///pyblog.db"
    # SMTP Server Setup
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = "True"
    MAIL_USERNAME = os.environ.get("PYBLOG_MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("PYBLOG_MAIL_PASSWORD")
