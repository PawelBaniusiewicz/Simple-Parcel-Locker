import logging
from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
from flask_migrate import Migrate
from app.db.configuration import db_uri, sa

def create_app() -> Flask:
    app = Flask(__name__)
    with app.app_context():
        #-----------------------------------------------
        # Configuring environment variables
        #-----------------------------------------------
        ENV_FILE = '.env'
        ENV_PATH = Path().cwd().absolute().joinpath(f'{ENV_FILE}')
        load_dotenv(ENV_PATH)

        # -----------------------------------------------
        # Configuring db connection
        # -----------------------------------------------
        #logging.info(db_uri)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(app)

        #migrate = Migrate(app, sa)

    return app