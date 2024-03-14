from os import environ
from typing import Callable

from requests import Session


def make_url(parent: str):
    def inner(endpoint: Callable):
        def wrapper(self, *args, **kwargs):
            base_url = environ.get('BACKEND_API_URL')
            endpoint_name = endpoint.__name__.replace('_', '-')

            self.url = f'{base_url}/api/{parent}/{endpoint_name}'
            print(self.url)

            return endpoint(self, *args, **kwargs)
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

        self.session = Session()
        self.access_token = ''

    @make_url('auth')
    def register(self,
                 name: str,
                 email: str,
                 password: str) -> tuple[bool, str]:
        data = {
            'name': name,
            'email': email,
            'password': password
        }

        response = self.session.post(self.url, data, verify=self.verify_ssl)
        if response.status_code != 200:
            return (False, response.json()['message'])

        self.access_token = response.json()['access_token']
        return (True, '')

    @make_url('auth')
    def login(self, email: str, password: str) -> tuple[bool, str]:
        data = {
            'email': email,
            'password': password
        }

        response = self.session.post(self.url, data, verify=self.verify_ssl)
        if response.status_code != 200:
            return (False, response.json()['message'])

        self.access_token = response.json()['access_token']
        return (True, '')

    @make_url('auth')
    def refresh_token(self) -> tuple[bool, str]:
        headers = {
            'X-CSRF-Token': self.session.cookies.get('csrf_token')
        }

        response = self.session.get(
            self.url,
            headers=headers,
            verify=self.verify_ssl
        )

        if response.status_code != 200:
            return (False, response.json()['message'])

        self.access_token = response.json()['access_token']
        return (True, '')
