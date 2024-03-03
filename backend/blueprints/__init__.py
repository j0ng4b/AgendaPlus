from enum import Enum
from typing import Any, Optional

from flask import Response, jsonify


class HTTPStatus(Enum):
    # 1xx Informational
    CONTINUE = 100
    SWITCHING_PROTOCOLS = 101
    PROCESSING = 102
    EARLY_HINTS = 103

    # 2xx Successful
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 209

    # 4xx Client error
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404


class BadAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST.value

    def __init__(self, message: str,
                 status_code: Optional[HTTPStatus] = None,
                 payload: Optional[dict[str, Any]] = None
                 ) -> None:
        self.message = message
        if status_code is not None:
            self.status_code = status_code.value

        self.payload = {}
        if payload is not None:
            self.payload = payload


    def to_dict(self) -> dict[str, Any]:
        response = {
            'message': self.message
        }

        response.update(self.payload)
        return response


def bad_api_usage_handler(exception: BadAPIUsage) -> tuple[Response, int]:
    return jsonify(exception.to_dict()), exception.status_code
