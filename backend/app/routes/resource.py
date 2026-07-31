from flask import Response, make_response, request, current_app, g
from flask_restful import Resource, reqparse
from jwt import ExpiredSignatureError

from ..service.configuration import user_service, parcel_service
from ..db.repository import user_repository, parcel_repository
from ..security.configuration import authorize
from ..service.dto import RegisterUserDto, ParcelDto
from ..models.enums import Roles, Status

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


class StatusResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('new_status', type=str, required=True)

    @authorize([Roles.ADMIN, Roles.USER, Roles.SUPPLIER])
    def patch(self, parcel_id: int) -> Response:
        args = StatusResource.parser.parse_args()
        new_status = args['new_status']
        user = g.current_user
        try:
            enum_status = Status(new_status)
            updated_parcel_dict = parcel_service.change_parcel_status(parcel_id, enum_status, user)
            return make_response(updated_parcel_dict, 200)

        except ValueError as e:
            return make_response({'message': str(e)}, 400)


class PickUpParcelResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number', type=str, help='Phone number cannot be empty', required=True)
    parser.add_argument('pickup_code', type=str, help='Pickup code cannot be empty', required=True)

    @authorize([Roles.USER])
    def post(self) -> Response:
        args = PickUpParcelResource.parser.parse_args()
        parcel = parcel_repository.find_parcel_by_phone_number_and_pickup_code(
            args['phone_number'],
            args['pickup_code']
        )
        if not parcel:
            return make_response({'message': 'Parcel not found or incorrect data'}, 404)

        try:
            parcel_service.change_parcel_status(parcel.id, Status.DELIVERED, parcel.receiver)
            return make_response(
                {'message': 'Parcel picked up successfully', 'parcel': ParcelDto.to_dict(parcel)},
                200)
        except ValueError as e:
            return make_response({'message': str(e)}, 400)

