from datetime import datetime
from typing import Optional

from flask import Blueprint, Response, jsonify, request
from kink import inject

from agendaplus.blueprints import BadAPIUsage, HTTPStatus, \
    bad_api_usage_handler
from agendaplus.models import Task
from agendaplus.security import authenticate
from agendaplus.services.task import ITaskService

task_bp = Blueprint('task', __name__, url_prefix='/task')
task_bp.register_error_handler(BadAPIUsage, bad_api_usage_handler)


@task_bp.route('/<int:task_id>', methods=['GET'])
@authenticate(pass_id='user_id')
@inject
def details(task_service: ITaskService,
            user_id: int,
            task_id: int) -> Response:
    task = task_service.get_by_user_by_id(user_id, task_id)
    if task is None:
        raise BadAPIUsage('task not found', status_code=HTTPStatus.NOT_FOUND)

    return jsonify({
        'status': 'success',
        'id': task.id,
        'date': task.date,
        'summary': task.summary,
        'description': task.description,
    })


@task_bp.route('/create', methods=['POST'])
@authenticate(pass_id='user_id')
@inject
def create(task_service: ITaskService, user_id: int) -> Response:
    date: Optional[str] = request.form.get('date', default=None)
    summary: Optional[str] = request.form.get('summary', default=None)
    description: Optional[str] = request.form.get('description', default=None)

    if summary is None or summary == '':
        raise BadAPIUsage('task summary is required')

    task_datetime = None
    if date is not None:
        task_datetime = datetime.fromisoformat(date)

    task = task_service.add(Task(summary, description, task_datetime, user_id))
    return jsonify({
        'status': 'success',
        'id': task.id,
    })


@task_bp.route('/update/<int:task_id>', methods=['PUT'])
@authenticate(pass_id='user_id')
@inject
def update(task_service: ITaskService, user_id: int, task_id: int) -> Response:
    date: Optional[str] = request.form.get('date', default=None)
    summary: Optional[str] = request.form.get('summary', default=None)
    description: Optional[str] = request.form.get('description', default=None)

    task = task_service.get_by_user_by_id(user_id, task_id)
    if task is None:
        raise BadAPIUsage(
            'can\'t update task, not found',
            status_code=HTTPStatus.NOT_FOUND
        )

    if date is not None:
        task.date = datetime.fromisoformat(date)

    if summary is not None:
        task.summary = summary

    if description is not None:
        task.description = description

    task_service.update(task)
    return jsonify({
        'status': 'success',
        'message': 'task updated',
    })


@task_bp.route('/delete/<int:task_id>', methods=['DELETE'])
@authenticate(pass_id='user_id')
@inject
def delete(task_service: ITaskService, user_id: int, task_id: int) -> Response:
    task = task_service.get_by_user_by_id(user_id, task_id)
    if task is None:
        raise BadAPIUsage('task not found', status_code=HTTPStatus.NOT_FOUND)

    task_service.delete(task_id)

    return jsonify({
        'status': 'success',
        'message': 'task deleted',
    })
