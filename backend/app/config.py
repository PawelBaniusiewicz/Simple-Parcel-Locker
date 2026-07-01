from dotenv import load_dotenv
from os import getenv

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