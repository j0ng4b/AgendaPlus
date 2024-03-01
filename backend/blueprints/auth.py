import os

from flask import Blueprint, Response, jsonify, request
from kink import inject

from backend.models import User
from backend.services.user import IUserService
from backend.security import jwt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
@inject
def register(user_service: IUserService) -> Response:
    name: str = request.form.get('name', None)
    email: str = request.form.get('email', None)
    password: str = request.form.get('password', None)

    if name is None or name == '':
        return jsonify({
            'sts': 'fail',
            'msg': 'user name not provided'
        })
    elif email is None or email == '':
        return jsonify({
            'sts': 'fail',
            'msg': 'user e-mail not provided'
        })
    elif password is None or password == '':
        return jsonify({
            'sts': 'fail',
            'msg': 'user password not provided'
        })

    # Check if user e-mail is already registered
    if user_service.get_by_email(email) is not None:
        return jsonify({
            'sts': 'fail',
            'msg': 'e-mail already in use'
        })

    # TODO: hash and salt password before add to database
    user_id = user_service.add(User(name, email, password)).id

    return jsonify({
        'sts': 'success',
        'tk': jwt.sign({
            'id': user_id,
            'name': name,
            'email': email
        }, secret_key=os.environ['SECRET_KEY'], expIn='15m')
    })


@auth_bp.route('/login', methods=['POST'])
@inject
def login(user_service: IUserService) -> Response:
    email: str = request.form.get('email', None)
    password: str = request.form.get('password', None)

    # Check if any field is empty
    if email is None or email == '':
        return jsonify({
            'sts': 'fail',
            'msg': 'user e-mail not provided'
        })
    elif password is None or password == '':
        return jsonify({
            'sts': 'fail',
            'msg': 'user password not provided'
        })

    if (user := user_service.get_by_email(email)) is None:
        return jsonify({
            'sts': 'fail',
            'msg': 'e-mail not registered'
        })

    # TODO: hash and salt password before compared with database ones
    if user.password != password:
        return jsonify({
            'sts': 'fail',
            'msg': 'wrong user e-mail or password'
        })

    # Create access token response
    return jsonify({
        'sts': 'success',
        'access_token': jwt.sign({
            'id': user.id,
            'name': user.name,
            'email': user.email
        }, secret_key=os.environ['AUTH_SECRET_KEY'], expIn='15m')
    })
