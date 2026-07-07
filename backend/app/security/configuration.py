from flask import request, make_response, current_app
from app.db.repository import user_repository
from jwt import ExpiredSignatureError
from functools import wraps
import logging
import jwt

logging.basicConfig(level=logging.INFO)

def authorize(roles: list[str] | None = None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                cookies = request.cookies.get('AccesToken')
                if not cookies:
                    return make_response({'message': 'Authorization failed'}, 401)


                access_token = cookies.split(' ')[1]
                decoded_access_token = jwt.decode(
                    access_token,
                    current_app.config['JWT_SECRET'],
                    algorithms=[current_app.config['JWT_AUTHTYPE']]
                )
                user = user_repository.find_by_id(int(decoded_access_token['sub']))

                if roles and str(user.role).lower() not in [role.lower() for role in roles]:
                    return make_response({'message': 'Access denied!'}, 403)

            except ExpiredSignatureError:
                return make_response({'message': 'Token expired'}, 401)

            except Exception as error:
                logging.info(repr(error))
                return make_response({'message': 'Access denied!'}, 401)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
