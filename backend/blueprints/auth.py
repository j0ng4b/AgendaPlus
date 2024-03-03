from typing import Optional

from flask import Blueprint, Response, jsonify, request, current_app
from kink import inject

from backend.blueprints import BadAPIUsage, HTTPStatus, bad_api_usage_handler
from backend.models import User
from backend.services.user import IUserService
from backend.security import jwt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_bp.register_error_handler(BadAPIUsage, bad_api_usage_handler)


@auth_bp.route('/register', methods=['POST'])
@inject
def register(user_service: IUserService) -> Response:
    config = current_app.config

    name: Optional[str] = request.form.get('name', None)
    email: Optional[str] = request.form.get('email', None)
    password: Optional[str] = request.form.get('password', None)

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

    return jsonify({
        'status': 'success',
        'access_token': jwt.sign({
                    'id': user_id,
                    'name': name,
                    'email': email
                },
                secret_key=str(config.get('AUTH_AT_SECRET_KEY')),
                expIn=str(config.get('AUTH_AT_EXPIRATION')))
    })


@auth_bp.route('/login', methods=['POST'])
@inject
def login(user_service: IUserService) -> Response:
    config = current_app.config

    email: Optional[str] = request.form.get('email', None)
    password: Optional[str] = request.form.get('password', None)

    if email is None or email == '':
        raise BadAPIUsage('user e-mail not provided')
    elif password is None or password == '':
        raise BadAPIUsage('user password not provided')

    if (user := user_service.get_by_email(email)) is None:
        raise BadAPIUsage('e-mail not registered',
                          status_code=HTTPStatus.NOT_FOUND)

    # TODO: hash and salt password before compared with database ones
    if user.password != password:
        raise BadAPIUsage('wrong password',
                          status_code=HTTPStatus.UNAUTHORIZED)

    return jsonify({
        'status': 'success',
        'access_token': jwt.sign({
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                },
                secret_key=str(config.get('AUTH_AT_SECRET_KEY')),
                expIn=str(config.get('AUTH_AT_EXPIRATION')))
    })
