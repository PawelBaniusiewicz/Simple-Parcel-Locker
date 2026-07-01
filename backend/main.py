from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate

from os import getenv
import logging

from app.db.entity import ParcelLockerEntity, ParcelEntity, LockerEntity, ActivationTokenEntity
from app.routes.resource import UserResource, ActivationUserResource
from app.mail.configuration import MailSender
from app.db.configuration import sa

from app.config import (
    db_uri,
    cors_config,
    mail_settings
)


logging.basicConfig(level=logging.INFO)

def create_app() -> Flask:
    app = Flask(__name__)
    with app.app_context():
        # -----------------------------------------------
        # Configuring CORS
        # -----------------------------------------------
        CORS(app, resources={'/*': cors_config})

        # -----------------------------------------------
        # Configuring db connection & migrations
        # -----------------------------------------------
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(app)

        migrate = Migrate(app, sa, compare_type=True)

        # -----------------------------------------------
        # Configuring mail
        # -----------------------------------------------
        app.config.update(mail_settings)
        MailSender(app, getenv('MAIL_USERNAME'))


        # -----------------------------------------------
        # Configuring routes
        # -----------------------------------------------
        api = Api(app)
        api.add_resource(UserResource, "/api/register")
        api.add_resource(ActivationUserResource, '/api/register/activate')

    return app