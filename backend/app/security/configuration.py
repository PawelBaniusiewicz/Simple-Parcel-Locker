from flask import request, make_response, current_app, g
from jwt import ExpiredSignatureError
from functools import wraps

from app.db.repository import user_repository
from ..models.enums import Roles

import jwt
import logging

logging.basicConfig(level=logging.INFO)

def authorize(roles: list[Roles] | None = None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                access_token = request.cookies.get('AccessToken')
                if not access_token:
                    return make_response({'message': 'Authorization failed'}, 401)

                decoded_access_token = jwt.decode(
                    access_token,
                    current_app.config['JWT_SECRET'],
                    algorithms=[current_app.config['JWT_AUTHTYPE']]
                )
                user = user_repository.find_by_id(int(decoded_access_token['sub']))
                g.current_user = user

                if roles and str(user.role.value).lower() not in [role.value.lower() for role in roles]:
                    return make_response({'message': 'Access denied!'}, 403)

            except ExpiredSignatureError:
                return make_response({'message': 'Token expired'}, 401)

            except Exception as error:
                logging.info(repr(error))
                return make_response({'message': 'Access denied!'}, 401)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
