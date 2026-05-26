from flask_restful import Resource, reqparse
from flask import Response
from ..service.dto import RegisterUserDto
from ..service.configuration import user_service

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