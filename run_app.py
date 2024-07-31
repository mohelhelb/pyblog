            
### IMPORTS  ################################################################### 

import os

from app import create_app
from config_app import config_env    


### RUN APP ####################################################################

app = create_app(ConfigClass=config_env[os.getenv("FLASK_ENV")])

if __name__ == "__main__":
    app.run()
