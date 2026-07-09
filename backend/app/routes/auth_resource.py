from flask_restful import Resource, reqparse
from flask import Response, make_response, current_app, request
from jwt import ExpiredSignatureError, InvalidTokenError

from app.db.repository import user_repository

import datetime
import jwt


class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help='Email cannot be empty')
    parser.add_argument('password', type=str, required=True, help='Password cannot be empty')

    def post(self) -> Response:
        args = LoginResource.parser.parse_args()
        email = args['email']
        password = args['password']

        user = user_repository.find_by_email(email)

        if not user:
            return make_response({'message': 'Authentication failed: Email not found'}, 400)

        if not user.is_active:
            return make_response({'message': 'Authentication failed: User is not active'}, 500)

        if not user.check_password(password):
            return make_response({'message': 'Authentication faild: Password incorrect'}, 400)

        access_token_exp = int((datetime.datetime.now(datetime.UTC) +
                                datetime.timedelta(minutes=int(current_app.config['JWT_ACCESS_MAX_AGE']))).timestamp())
        refresh_token_exp = int((datetime.datetime.now(datetime.UTC) +
                                datetime.timedelta(minutes=int(current_app.config['JWT_REFRESH_MAX_AGE']))).timestamp())

        access_token_payload = {
            'iat': datetime.datetime.now(datetime.UTC),
            'exp': access_token_exp,
            'sub': str(user.id),
        }

        refresh_token_payload = {
            'iat': datetime.datetime.now(datetime.UTC),
            'exp': refresh_token_exp,
            'sub': str(user.id),
            'access_token_exp': access_token_exp
        }

        access_token = jwt.encode(access_token_payload, current_app.config['JWT_SECRET'],
                                  algorithm=current_app.config['JWT_AUTHTYPE'])
        refresh_token = jwt.encode(refresh_token_payload, current_app.config['JWT_SECRET'],
                                   algorithm=current_app.config['JWT_AUTHTYPE'])

        response = make_response({'message': 'Successfully logged in'}, 200)
        response.set_cookie('AccessToken', access_token, httponly=True)
        response.set_cookie('RefreshToken', refresh_token, httponly=True)

        return response

class LogoutResource(Resource):
    def post(self) -> Response:
        response = make_response({'message': 'Logged Out'}, 200)
        response.delete_cookie('AccessToken')
        response.delete_cookie('RefreshToken')
        return response

class RefreshTokensResource(Resource):
    def post(self) -> Response:
        refresh_token = request.cookies.get('RefreshToken')

        if not refresh_token:
            return make_response({'message': 'Refresh token is missing'}, 401)

        try:
            decoded_refresh_token = jwt.decode(
                refresh_token,
                current_app.config['JWT_SECRET'],
                algorithms=[current_app.config['JWT_AUTHTYPE']]
            )
        except ExpiredSignatureError:
            return make_response({'message': 'Refresh token has expired, please log in again'}, 401)
        except InvalidTokenError:
            return make_response({'message': 'Invalid refresh token'}, 401)

        new_access_token_exp = int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            minutes=int(current_app.config['JWT_ACCESS_MAX_AGE']))).timestamp())

        accces_token_payload = {
            'iat': datetime.datetime.now(datetime.UTC),
            'exp': new_access_token_exp,
            'sub': str(decoded_refresh_token['sub']),
        }

        refresh_token_payload = {
            'iat': decoded_refresh_token['iat'],
            'exp': decoded_refresh_token['exp'],
            'sub': str(decoded_refresh_token['sub']),
            'access_token_exp': new_access_token_exp
        }
        access_token = jwt.encode(accces_token_payload, current_app.config['JWT_SECRET'],
                                  algorithm=current_app.config['JWT_AUTHTYPE'])
        refresh_token = jwt.encode(refresh_token_payload, current_app.config['JWT_SECRET'],
                                   algorithm=current_app.config['JWT_AUTHTYPE'])

        response = make_response({'message': 'Tokens have been successfully refreshed'}, 201)
        response.set_cookie('AccessToken', access_token, httponly=True)
        response.set_cookie('RefreshToken', refresh_token, httponly=True)

        return response

