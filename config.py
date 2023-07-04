import os

class Config:
    pass

class DevelopmentConfig(Config):
    # If the environment variable, PYBLOG_SECRET_KEY, exists and is not empty, assign SECRET_KEY to its value.
    # Otherwise, assign SECRET_KEY to "development".
    SECRET_KEY = os.environ.get("PYBLOG_SECRET_KEY") or "development"
