
import os

from app import create_app
from app.config import config_env

app = create_app(ConfigClass=config_env[os.getenv("FLASK_ENV")])

if __name__ == "__main__":
    app.run()
