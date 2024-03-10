from base64 import urlsafe_b64decode, urlsafe_b64encode
import hashlib
import hmac
import json
import time
from typing import Any, Dict, List, Union, cast

JSONType = Dict[str, Union[str, int, float, bool, Dict[str, Any], List[Any]]]


class JWTInvalidToken(Exception):
    pass


class JWTExpiredToken(Exception):
    pass


def _base64_url_encode(string: str | bytes) -> str:
    encoded: bytes

    if isinstance(string, str):
        encoded = string.encode()
    else:
        encoded = string

    return urlsafe_b64encode(encoded).decode().rstrip('=')


def _base64_url_decode(string: str | bytes) -> str:
    if isinstance(string, str):
        string += '=' * (4 - (len(string) % 4))
        string = string.encode()
    else:
        string += b'=' * (4 - (len(string) % 4))

    return urlsafe_b64decode(string).decode()


def sign(payload: Dict[str, object], secret_key: str, **kwargs: str) -> str:
    # Encode header
    header_base64: str = _base64_url_encode(json.dumps({
        'typ': 'JWT',
        'alg': 'HS256'
    }, separators=(',', ':')))

    # Include expiration time
    if 'expIn' in kwargs:
        expire: int

        if str(kwargs['expIn']).endswith('d'):      # days
            expire = int(kwargs['expIn'][:-1]) * 86_400
        elif str(kwargs['expIn']).endswith('h'):    # hours
            expire = int(kwargs['expIn'][:-1]) * 3_600
        elif str(kwargs['expIn']).endswith('m'):    # minutes
            expire = int(kwargs['expIn'][:-1]) * 60
        elif str(kwargs['expIn']).endswith('s'):    # seconds
            expire = int(kwargs['expIn'][:-1])
        else:                                       # also seconds
            expire = int(kwargs['expIn'])

        payload['exp'] = int(time.time()) + expire

    if 'iat' not in payload:
        payload['iat'] = int(time.time())

    # Encode payload
    payload_base64: str = _base64_url_encode(json.dumps(payload,
                                                        separators=(',', ':')))

    # Generate signature
    header_payload: bytes = f'{header_base64}.{payload_base64}'.encode()
    signature: bytes = hmac.digest(secret_key.encode(), header_payload,
                                   hashlib.sha256)

    # Encode signature
    signature_base64: str = _base64_url_encode(signature)

    return f'{header_base64}.{payload_base64}.{signature_base64}'


def verify(token: str, secret_key: str) -> JSONType:
    # Split token parts
    token_parts: List[str] = token.split('.')

    if len(token_parts) != 3:
        raise JWTInvalidToken('token not following the correct'
                              ' header.payload.signature JWT structure')

    # If expire time was defined check if the token has expired
    payload: JSONType = json.loads(_base64_url_decode(token_parts[1]))
    if 'exp' in payload:
        if cast(int, payload['exp']) - int(time.time()) < 0:
            raise JWTExpiredToken('the token is no more valid')

    header_payload: bytes = f'{token_parts[0]}.{token_parts[1]}'.encode()
    signature: bytes = hmac.digest(secret_key.encode(),
                                   header_payload,
                                   hashlib.sha256)

    signature_base64: str = _base64_url_encode(signature)
    if signature_base64 != token_parts[2]:
        raise JWTInvalidToken('wrong token signature')

    return payload
