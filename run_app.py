
import os

from pyblog import create_app
from pyblog.config import config_env

app = create_app(ConfigClass=config_env[os.getenv("FLASK_ENV")])

if __name__ == "__main__":
    app.run()
