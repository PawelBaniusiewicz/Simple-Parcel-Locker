from flask import Response, make_response, request, current_app, g
from flask_restful import Resource, reqparse
from jwt import ExpiredSignatureError

from ..service.configuration import user_service, parcel_service
from ..db.repository import user_repository
from ..security.configuration import authorize
from ..service.dto import RegisterUserDto
from ..models.enums import Roles

import logging
import jwt

logging.basicConfig(level=logging.INFO)

class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='Name cannot be empty')
    parser.add_argument('email', type=str, required=True, help='Email cannot be empty')
    parser.add_argument('password', type=str, required=True, help='Password cannot be empty')
    parser.add_argument('password_confirmation', type=str, required=True, help='Password confirmation cannot be empty')
    parser.add_argument('phone_number', type=str, required=True, help='Phone number cannot be empty')

    def post(self) -> Response:
        register_user_dto = RegisterUserDto.from_dict(UserResource.parser.parse_args())
        return user_service.register_user(register_user_dto)

class ActivationUserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('token', type=str, required=True, help='Token cannot be empty')

    def post(self) -> Response:
        json_body = ActivationUserResource.parser.parse_args()
        return user_service.active_user(json_body['token'])

class UserMeResource(Resource):
    def get(self) -> Response:
        access_token = request.cookies.get('AccessToken')

        if not access_token:
            return make_response({'isAuthenticated': False, 'user': None}, 200)

        try:
            decoded_access_token = jwt.decode(
                access_token,
                current_app.config['JWT_SECRET'],
                algorithms=[current_app.config['JWT_AUTHTYPE']]
            )

            user = user_repository.find_by_id(int(decoded_access_token['sub']))

            if not user or not user.is_active:
                return make_response({'isAuthenticated': False, 'user': None}, 200)

            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': str(user.role.value)
            }
            return make_response({'isAuthenticated': True, 'user': user_data}, 200)

        except ExpiredSignatureError:
            return make_response({'message': 'Token expired'}, 401)

        except Exception:
            return make_response({'isAuthenticated': False, 'user': None}, 200)


class ParcelResource(Resource):

    @authorize([Roles.ADMIN, Roles.USER])
    def get(self) -> Response:
        user = g.current_user
        parcels = parcel_service.get_users_parcels(user.id)
        return make_response({'parcels': [parcel for parcel in parcels]})

