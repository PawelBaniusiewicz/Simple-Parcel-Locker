from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
from flask_migrate import Migrate
from app.db.configuration import sa
from os import getenv
from app.db.entity import ParcelLockerEntity, ParcelEntity, LockerEntity
from app.routes.resource import UserResource
from flask_restful import Api
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.INFO)

def create_app() -> Flask:
    app = Flask(__name__)
    with app.app_context():
        # -----------------------------------------------
        # Configuring environment variables
        # -----------------------------------------------
        ENV_FILE = '.env'
        ENV_PATH = Path().cwd().absolute().joinpath(f'{ENV_FILE}')
        load_dotenv(ENV_PATH)

        # -----------------------------------------------
        # Configuring CORS
        # -----------------------------------------------
        cors_config = {
            'allow_headers': [
                'accept',
                'accept-encoding',
                'authorization',
                'content-type'
            ],
            'methods': [
                'delete',
                'get',
                'post',
                'patch',
                'put',
                'options'
            ],
            'origins': [
                f'{getenv('CORS_ORIGIN')}'
            ]
        }
        CORS(app, resources={'/*': cors_config})

        # -----------------------------------------------
        # Configuring db connection & migrations
        # -----------------------------------------------

        db_username = getenv('DB_USERNAME')
        db_password = getenv('DB_PASSWORD')
        db_name = getenv('DB_NAME')
        db_port = getenv('DB_PORT')
        db_hostname = getenv('DB_HOSTNAME')
        db_uri = f"mysql+mysqldb://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}"
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(app)

        migrate = Migrate(app, sa)

        api = Api(app)
        api.add_resource(UserResource, "/api/register")

        #TODO:
        # 1. trzeba ogarnąć routes do rejestracji usera bo to co mam może być złe
        # 2. Dokończyć nagranie 14 zacząć od 31 minuty
        # 3. Sprawdzić czy to co zrobiłem działa
    return app