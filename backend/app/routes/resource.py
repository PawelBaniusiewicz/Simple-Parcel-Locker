from flask import Response, make_response, request, current_app, g
from flask_restful import Resource, reqparse
from jwt import ExpiredSignatureError

from ..db.entity import ParcelLockerEntity
from ..service.configuration import user_service, parcel_service, parcel_locker_service
from ..db.repository import user_repository, parcel_repository, parcel_locker_repository
from ..security.configuration import authorize
from ..service.dto import RegisterUserDto, ParcelDto, ParcelLockerDto
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


class SupplierBulkStatusResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('tracking_numbers', type=str, action='append', help="List of parcels id cannot be empty")
    parser.add_argument('status', type=str, help="Status cannot be empty")

    @authorize([Roles.SUPPLIER])
    def post(self) -> Response:
        args = SupplierBulkStatusResource.parser.parse_args()
        user = g.current_user

        try:
            target_status = Status(args['status'])
        except ValueError:
            return make_response({'message': f"Invalid status: {args['status']}"}, 400)
        
        success_count = 0
        errors = []

        for tracking_number in args['tracking_numbers']:
            parcel = parcel_repository.find_by_tracking_number(tracking_number)

            if not parcel:
                errors.append({"tracking_number": tracking_number, "error": "Parcel not found in system."})
                continue

            try:
                parcel_service.change_parcel_status(parcel.id, target_status, user)
                success_count += 1
            except ValueError as e:
                errors.append({"tracking_number": tracking_number, "error": str(e)})

        return make_response({
            'message': f"Successfully updated {success_count} parcels."}
                    if errors == [] else {
                        'message': f"Successfully updated {success_count} parcels.",
                        'errors': errors
                    }
            )


class ParcelLockerResource(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument('id', type=int, location='args', required=False, help="Optional Parcel locker ID")

    post_parser = reqparse.RequestParser()
    post_parser.add_argument('name', type=str, required=True, help="Name cannot be null or empty")
    post_parser.add_argument('address', type=str, required=True, help="Address cannot be null or empty")
    post_parser.add_argument('latitude', type=float, required=True, help="Latitude cannot be null or empty")
    post_parser.add_argument('longitude', type=float, required=True, help="Longitude cannot be null or empty")

    def get(self) -> Response:
        args = self.get_parser.parse_args()
        parcel_locker_id = args.get('id')

        try:
            if parcel_locker_id:
                parcel_locker = parcel_locker_service.get_parcel_locker_by_id(parcel_locker_id)
                return make_response(parcel_locker.to_dict(), 200)
            else:
                parcel_lockers = parcel_locker_service.get_all_parcel_lockers()
                if not parcel_lockers:
                    return make_response([])
                return make_response([locker.to_dict() for locker in parcel_lockers], 200)

        except ValueError as ve:
            return make_response({"message": str(ve)}, 404)
        except Exception as e:
            return make_response({"message": f"Error fetching parcel lockers: {str(e)}"}, 500)

    @authorize([Roles.ADMIN])
    def post(self) -> Response:
        args = self.post_parser.parse_args()

        try:
            new_locker_dto = parcel_locker_service.add_parcel_locker(
                name=args['name'],
                address=args['address'],
                latitude=args['latitude'],
                longitude=args['longitude']
            )
            return make_response({
                "message": "Parcel locker created successfully",
                "parcel_locker": new_locker_dto.to_dict()
            }, 201)

        except ValueError as ve:
            return make_response({"message": str(ve)}, 400)
        except Exception as e:
            return make_response({"message": f"Error creating parcel locker: {str(e)}"}, 500)
