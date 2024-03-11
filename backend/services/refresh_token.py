from abc import ABC, abstractmethod
from os import environ
from time import time
from typing import Any, cast
from uuid import uuid4

from kink import inject

from backend.models import RefreshToken
from backend.security import jwt
from backend.unit_of_work import IUnitOfWork


class IRefreshTokenService(ABC):
    _uow: IUnitOfWork

    @abstractmethod
    def generate(self, user_id: int) -> tuple[str, str]:
        raise NotImplementedError

    @abstractmethod
    def verify(self, refresh_token: str, csrf_token: str) -> tuple[bool, Any]:
        raise NotImplementedError


@inject
class RefreshTokenService(IRefreshTokenService):
    def __init__(self, uow: IUnitOfWork) -> None:
        self._uow = uow

    def generate(self, user_id: int) -> tuple[str, str]:
        csrf_token = uuid4().hex

        iat = int(time())
        refresh_token = jwt.sign({
                'id': user_id,
                'csrf': csrf_token,
                'iat': iat
            },
            secret_key=str(environ.get('AUTH_RT_SECRET_KEY')),
            expIn=str(environ.get('AUTH_RT_EXPIRATION'))
        )

        token = self._uow.refresh_token.get_by_user_id(user_id)
        if token is None:
            self._uow.refresh_token.add(RefreshToken(iat, user_id))
        else:
            token.iat = iat
            self._uow.refresh_token.update(token)

        return (refresh_token, csrf_token)

    def verify(self, refresh_token: str, csrf_token: str) -> tuple[bool, Any]:
        try:
            payload = jwt.verify(
                refresh_token,
                secret_key=str(environ.get('AUTH_RT_SECRET_KEY'))
            )
        except jwt.JWTInvalidToken:
            return (False, 'invalid token')
        except jwt.JWTExpiredToken:
            return (False, 'expired token')

        if payload['csrf'] != csrf_token:
            return (False, 'refresh token\'s claim for CSRF token doesn\'t '
                           'match the header CSRF token')

        # The below code will check for token reuse
        token = self._uow.refresh_token.get_by_user_id(cast(int,
                                                            payload['id']))
        if token is not None:
            if token.iat > cast(int, payload['iat']):
                return (False, 'refresh token reuse')

        return (True, payload)
