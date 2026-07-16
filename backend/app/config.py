from dotenv import load_dotenv
from os import getenv

from app.models.enums import Status

load_dotenv(override=True)

# -----------------------------------------------
# Configuring db connection & migrations
# -----------------------------------------------

db_username = getenv('DB_USERNAME')
db_password = getenv('DB_PASSWORD')
db_name = getenv('DB_NAME')
db_port = getenv('DB_PORT')
db_hostname = getenv('DB_HOSTNAME')
db_uri = f"mysql+mysqldb://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}"

# -----------------------------------------------
# Configuring CORS
# -----------------------------------------------
cors_config = {
    'allow_headers': [
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'Access-Control-Allow-Credentials'
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
    ],
    'supports_credentials': True,
}

# -----------------------------------------------
# Configuring mail
# -----------------------------------------------
mail_settings = {
    'MAIL_SERVER': getenv('MAIL_SERVER'),
    'MAIL_PORT': int(getenv('MAIL_PORT', 465)),
    'MAIL_USE_SSL': bool(getenv('MAIL_USE_SSL')),
    'MAIL_USERNAME': getenv('MAIL_USERNAME'),
    'MAIL_PASSWORD': getenv('MAIL_PASSWORD'),
}

# -----------------------------------------------
# Activation Token
# -----------------------------------------------
ACTIVATION_TOKEN_EXPIRATION_TIME_IN_SECONDS = int(getenv('ACTIVATION_TOKEN_EXPIRATION_TIME_IN_SECONDS', '300'))
ACTIVATION_TOKEN_LENGTH = int(getenv('ACTIVATION_TOKEN_LENGTH', '30'))

# -----------------------------------------------------------------------------------------
# JWT Configuartion
# -----------------------------------------------------------------------------------------
JWT_CONFIG = {
    'JWT_ISSUER': getenv('JWT_ISSUER'),
    'JWT_AUTHTYPE': getenv('JWT_AUTHTYPE'),
    'JWT_SECRET': getenv('JWT_SECRET'),
    'JWT_ACCESS_MAX_AGE': getenv('JWT_ACCESS_MAX_AGE'),
    'JWT_REFRESH_MAX_AGE': getenv('JWT_REFRESH_MAX_AGE'),
    'JWT_PREFIX': getenv('JWT_PREFIX', 'Bearer '),
}

# -----------------------------------------------
# Configuration of subsequent parcel status states
# -----------------------------------------------
ALLOWED_TRANSITIONS = {
    Status.LABEL_CREATED: [Status.PENDING],
    Status.PENDING: [Status.IN_TRANSIT],
    Status.IN_TRANSIT: [Status.IN_WAREHOUSE, Status.READY_FOR_PICKUP],
    Status.IN_WAREHOUSE: [Status.OUT_FOR_DELIVERY],
    Status.OUT_FOR_DELIVERY: [Status.READY_FOR_PICKUP],
    Status.READY_FOR_PICKUP: [Status.DELIVERED, Status.EXPIRED],
    Status.EXPIRED: [Status.RETURNED],
    Status.DELIVERED: [],
    Status.RETURNED: []
}
