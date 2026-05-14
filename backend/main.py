from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
from flask_migrate import Migrate
from app.db.configuration import sa
from os import getenv
from app.db.entity import ParcelLockerEntity, ParcelEntity, LockerEntity
import logging

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
        # Configuring db connection & migrations
        # -----------------------------------------------

        db_username = getenv('DB_USERNAME')
        db_password = getenv('DB_PASSWORD')
        db_name = getenv('DB_NAME')
        db_port = getenv('DB_PORT')
        db_hostname = getenv('DB_HOSTNAME')
        db_uri = f"mysql+mysqldb://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}"
        logging.info(db_uri)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(app)

        migrate = Migrate(app, sa)

    return app