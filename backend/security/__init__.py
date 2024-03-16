import functools
from os import environ
from typing import Any, Callable

from flask import Response, request

from backend.blueprints import BadAPIUsage, HTTPStatus
from backend.security import jwt


def authenticate(function: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(function)
    def wrapper(*args: list[Any], **kwargs: dict[str, Any]) -> Any:
        header = request.headers.get('Authorization')
        if header is None:
            raise BadAPIUsage('no authorization token provided')

        if not header.startswith('Bearer'):
            raise BadAPIUsage(
                'invalid authorization method',
                status_code=HTTPStatus.UNAUTHORIZED
            )

        try:
            jwt.verify(
                header[7:],
                secret_key=str(environ.get('AUTH_AT_SECRET_KEY'))
            )
        except jwt.JWTInvalidToken:
            raise BadAPIUsage(
                'invalid access token',
                status_code=HTTPStatus.UNAUTHORIZED
            )
        except jwt.JWTExpiredToken:
            raise BadAPIUsage(
                'expired access token',
                status_code=HTTPStatus.UNAUTHORIZED
            )

        return function(*args, **kwargs)
    return wrapper
