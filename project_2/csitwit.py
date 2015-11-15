from flask import Flask
from helpers import functions, init
import router

# create our application
app = Flask(__name__)

# configuration
app.config.update(
    DEBUG      =  True,
    DATABASE   =  'minitwit.db',
    SECRET_KEY =  'a unique key'
)

# some initialization functions
init.start(app)

# set our router
router.set_router(app)

if __name__ == "__main__":
    app.run(port=5001)


