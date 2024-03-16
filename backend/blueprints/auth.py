from os import environ
from typing import Optional

from flask import Blueprint, Response, jsonify, request
from kink import inject

from backend.blueprints import BadAPIUsage, HTTPStatus, bad_api_usage_handler
from backend.models import User
from backend.security import jwt
from backend.services.refresh_token import IRefreshTokenService
from backend.services.user import IUserService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_bp.register_error_handler(BadAPIUsage, bad_api_usage_handler)


@auth_bp.route('/register', methods=['POST'])
@inject
def register(user_service: IUserService,
             refresh_token_service: IRefreshTokenService) -> Response:
    name: Optional[str] = request.form.get('name', default=None)
    email: Optional[str] = request.form.get('email', default=None)
    password: Optional[str] = request.form.get('password', default=None)

    if name is None or name == '':
        raise BadAPIUsage('user name not provided')
    elif email is None or email == '':
        raise BadAPIUsage('user e-mail not provided')
    elif password is None or password == '':
        raise BadAPIUsage('user password not provided')

    if user_service.get_by_email(email) is not None:
        raise BadAPIUsage('e-mail already in use')

    # TODO: hash and salt password before add to database
    user_id = user_service.add(User(name, email, password)).id

    response: Response = jsonify({
        'id': user_id,
        'email': email,
        'status': 'success',
        'access_token': jwt.sign({
                    'id': user_id,
                    'email': email
                },
                secret_key=str(environ.get('AUTH_AT_SECRET_KEY')),
                expIn=str(environ.get('AUTH_AT_EXPIRATION')))
    })

    refresh_token, csrf_token = refresh_token_service.generate(user_id)
    response.set_cookie('csrf_token', value=csrf_token, secure=True)
    response.set_cookie(
        'refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True
    )

    return response


@auth_bp.route('/login', methods=['POST'])
@inject
def login(user_service: IUserService,
          refresh_token_service: IRefreshTokenService) -> Response:
    email: Optional[str] = request.form.get('email', default=None)
    password: Optional[str] = request.form.get('password', default=None)

    if email is None or email == '':
        raise BadAPIUsage('user e-mail not provided')
    elif password is None or password == '':
        raise BadAPIUsage('user password not provided')

    if (user := user_service.get_by_email(email)) is None:
        raise BadAPIUsage(
            'e-mail not registered',
            status_code=HTTPStatus.NOT_FOUND
        )

    # TODO: hash and salt password before compared with database ones
    if user.password != password:
        raise BadAPIUsage(
            'wrong password',
            status_code=HTTPStatus.UNAUTHORIZED
        )

    response: Response = jsonify({
        'id': user.id,
        'email': email,
        'status': 'success',
        'access_token': jwt.sign({
                    'id': user.id,
                    'email': user.email
                },
                secret_key=str(environ.get('AUTH_AT_SECRET_KEY')),
                expIn=str(environ.get('AUTH_AT_EXPIRATION')))
    })

    refresh_token, csrf_token = refresh_token_service.generate(user.id)

    response.set_cookie('csrf_token', value=csrf_token, secure=True)
    response.set_cookie(
        'refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True
    )

    return response


@auth_bp.route('/refresh-token', methods=['GET'])
@inject
def refresh_token(user_service: IUserService,
                  refresh_token_service: IRefreshTokenService) -> Response:
    csrf_token = request.headers.get('X-CSRF-Token', None)
    if csrf_token is None:
        raise BadAPIUsage(
            'invalid CSRF token',
            status_code=HTTPStatus.FORBIDDEN
        )

    refresh_token = request.cookies.get('refresh_token', default=None)
    if refresh_token is None:
        raise BadAPIUsage(
            'invalid refresh token',
            status_code=HTTPStatus.FORBIDDEN
        )

    valid, result = refresh_token_service.verify(refresh_token, csrf_token)
    if not valid:
        raise BadAPIUsage(result, status_code=HTTPStatus.UNAUTHORIZED)

    user = user_service.get_by_id(result['id'])
    if user is None:
        raise BadAPIUsage(
            'user not found',
            status_code=HTTPStatus.NOT_FOUND
        )

    response: Response = jsonify({
        'id': user.id,
        'email': user.email,
        'status': 'success',
        'access_token': jwt.sign({
                    'id': user.id,
                    'email': user.email
                },
                secret_key=str(environ.get('AUTH_AT_SECRET_KEY')),
                expIn=str(environ.get('AUTH_AT_EXPIRATION')))
    })

    refresh_token, csrf_token = refresh_token_service.generate(user.id)
    response.set_cookie('csrf_token', value=csrf_token, secure=True)
    response.set_cookie(
        'refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True
    )

    return response
