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
    if 'name' not in request.form:
        return jsonify({
            'sts': 'fail',
            'msg': 'user name not provided'
        })
    elif 'email' not in request.form:
        return jsonify({
            'sts': 'fail',
            'msg': 'user e-mail not provided'
        })
    elif 'password' not in request.form:
        return jsonify({
            'sts': 'fail',
            'msg': 'user password not provided'
        })

    name: str = request.form['name']
    email: str = request.form['email']
    password: str = request.form['password']

    if user_service.get_by_email(email) is not None:
        return jsonify({
            'sts': 'fail',
            'msg': 'e-mail already in use'
        })

    # TODO: hash and salt password before save on database
    user_service.add(User(name, email, password))

    return jsonify({
        'sts': 'success',
        'tk': jwt.sign({
            'name': name,
            'email': email
        }, secret_key=os.environ['SECRET_KEY'], expIn='15m')
    })


@auth_bp.route('/login', methods=['GET'])
@inject
def login(user_service: IUserService) -> Response:
    if 'email' not in request.form:
        return jsonify({
            'sts': 'fail',
            'msg': 'user e-mail not provided'
        })
    elif 'password' not in request.form:
        return jsonify({
            'sts': 'fail',
            'msg': 'user password not provided'
        })

    email: str = request.form['email']
    password: str = request.form['password']

    if (user := user_service.get_by_email(email)) is None:
        return jsonify({
            'sts': 'fail',
            'msg': 'e-mail not registered'
        })

    # TODO: hash and salt password before compared with database ones
    if user.password != password:
        return jsonify({
            'sts': 'fail',
            'msg': 'wrong user password'
        })

    return jsonify({
        'sts': 'success',
        'tk': jwt.sign({
            'name': user.name,
            'email': email
        }, secret_key=os.environ['SECRET_KEY'], expIn='15m')
    })
