from flask_apscheduler import APScheduler
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask import Flask
from os import getenv
import logging

from app.db.entity import (
    ParcelLockerEntity,
    ParcelEntity,
    LockerEntity,
    ActivationTokenEntity
)
from app.routes.auth_resource import (
    LoginResource,
    RefreshTokensResource,
    LogoutResource
)
from app.routes.resource import (
    UserResource,
    ActivationUserResource,
    UserMeResource,
    ParcelResource,
    StatusResource,
    PickUpParcelResource,
    SupplierBulkStatusResource
)
from app.scheduler.configuration import scheduler
from app.mail.configuration import MailSender
from app.db.configuration import sa
from app.config import JWT_CONFIG

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

        # -----------------------------------------------------------------------------------------
        # JWT Configuartion
        # -----------------------------------------------------------------------------------------
        app.config.update(JWT_CONFIG)

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
        # Scheduler configuration
        # -----------------------------------------------
        app.config['SCHEDULER_API_ENABLED'] = True
        scheduler.init_app(app)
        scheduler.start()


        # -----------------------------------------------
        # Configuring routes
        # -----------------------------------------------
        api = Api(app)
        api.add_resource(UserResource, "/api/register")
        api.add_resource(UserMeResource, '/api/me')
        api.add_resource(ActivationUserResource, '/api/register/activate')
        api.add_resource(RefreshTokensResource, '/api/refresh')
        api.add_resource(LoginResource, '/api/login')
        api.add_resource(LogoutResource, '/api/logout')
        api.add_resource(ParcelResource, '/api/my_packages')
        api.add_resource(StatusResource, '/api/parcels/<int:parcel_id>/status')
        api.add_resource(PickUpParcelResource, '/api/pickup_parcel')
        api.add_resource(SupplierBulkStatusResource, '/api/courier/parcels/status')

    return app