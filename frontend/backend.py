from os import environ
from typing import Any, Callable, Optional

import requests


def make_url(parent: str, endpoint: Optional[str] = None, auth: bool = True):
    def inner(function: Callable):
        def wrapper(self, *args, **kwargs):
            base_url = environ.get('BACKEND_API_URL')

            if endpoint is None:
                endpoint_name = function.__name__.replace('_', '-')
            else:
                endpoint_name = endpoint

            self.url = f'{base_url}/api/{parent}/{endpoint_name}'

            self.headers = {}
            if auth and self.access_token != '':
                self.headers = {
                    'Authorization': f'Bearer {self.access_token}'
                }

            return function(self, *args, **kwargs)
        return wrapper
    return inner


class AgendaPlusAPI:
    def __init__(self):
        env = environ.get('RUN_ENV', default='Development')
        verify_ssl = environ.get('VERIFY_SSL_CERTIFICATES', default=None)

        self.verify_ssl = True
        if env == 'Production' or verify_ssl == 'False':
            self.verify_ssl = False

        # This is used on endpoints. If using make_url function decorator this
        # attribute is automatic updated
        self.url = ''

        # This is used on endpoints. If using make_url function decorator this
        # attribute is automatic updated to set authentication
        self.headers = {}

        self.session = requests.Session()
        self.access_token = ''

    @make_url('auth', auth=False)
    def register(self,
                 name: str,
                 email: str,
                 password: str) -> dict[str, Any]:
        data = {
            'name': name,
            'email': email,
            'password': password
        }

        response = self.session.post(self.url, data, verify=self.verify_ssl)
        if response.status_code != 200:
            return response.json()

        response_json = response.json()
        self.access_token = response_json.get('access_token')

        response_json.pop('access_token')
        return response_json

    @make_url('auth', auth=False)
    def login(self, email: str, password: str) -> dict[str, Any]:
        data = {
            'email': email,
            'password': password
        }

        response = self.session.post(self.url, data, verify=self.verify_ssl)
        if response.status_code != 200:
            return response.json()

        response_json = response.json()
        self.access_token = response_json.get('access_token')

        response_json.pop('access_token')
        return response_json

    @make_url('auth', endpoint='refresh-token', auth=False)
    def __refresh_token(self) -> bool:
        response = self.session.get(
            self.url,
            headers={'X-CSRF-Token': self.session.cookies.get('csrf_token')},
            verify=self.verify_ssl
        )

        if response.status_code != 200:
            return False

        self.access_token = response.json().get('access_token')
        return True

        response_json.pop('access_token')
        return (True, response_json)
