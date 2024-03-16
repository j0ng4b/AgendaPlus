from typing import Optional

from flask import Blueprint, Response, jsonify, request
from kink import inject

from backend.blueprints import BadAPIUsage, HTTPStatus, bad_api_usage_handler
from backend.security import authenticate
from backend.services.task import ITaskService
from backend.services.user import IUserService

user_bp = Blueprint('user', __name__, url_prefix='/user')
user_bp.register_error_handler(BadAPIUsage, bad_api_usage_handler)


@user_bp.route('/', methods=['GET'])
@authenticate(pass_id='user_id')
@inject
def index(user_service: IUserService, user_id: int) -> Response:
    user = user_service.get_by_id(user_id)
    if user is None:
        raise BadAPIUsage('user not found', status_code=HTTPStatus.NOT_FOUND)

    return jsonify({
        'status': 'success',
        'id': user.id,
        'name': user.name,
        'email': user.email
    })


@user_bp.route('/rename', methods=['PATCH'])
@authenticate(pass_id='user_id')
@inject
def rename(user_service: IUserService, user_id: int) -> Response:
    user = user_service.get_by_id(user_id)
    if user is None:
        raise BadAPIUsage('user not found', status_code=HTTPStatus.NOT_FOUND)

    new_name: Optional[str] = request.form.get('name', default=None)
    if new_name is None or new_name == '':
        raise BadAPIUsage('new user name not provided')

    user.name = new_name
    user_service.update(user)

    return jsonify({
        'status': 'success',
        'id': user.id,
        'name': user.name,
        'email': user.email
    })


@user_bp.route('/tasks', methods=['GET'])
@authenticate(pass_id='user_id')
@inject
def tasks(task_service: ITaskService, user_id: int) -> Response:
    tasks = task_service.get_by_user_id(user_id)
    return jsonify({
        'status': 'success',
        'tasks': tasks
    })
