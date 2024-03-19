import os
from typing import Optional, cast

from dotenv import load_dotenv

from agendaplus import create_app


def main() -> None:
    # Load environment variables from .env files
    load_dotenv('.env.shared')
    load_dotenv('.env.backend')

    if os.environ.get('RUN_ENV', default='Development') == 'Production':
        return

    # Debug server port
    SERVER_PORT = os.environ.get('SERVER_PORT', default=5000)

    # Try to find SSL certificate and key
    ssl_context: Optional[tuple[str, str] | list[str]] = [
        str(os.environ.get('SERVER_SSL_CERTIFICATE', default='')),
        str(os.environ.get('SERVER_SSL_CERTIFICATE_KEY', default=''))
    ]

    if ssl_context is None or ssl_context[0] == '' or ssl_context[1] == '':
        ssl_context = None
        print(' * Running development server in HTTP')
    else:
        ssl_context = (ssl_context[0], ssl_context[1])
        print(' * Running development server in HTTPS')

    app = create_app()
    app.run(port=cast(int, SERVER_PORT), debug=True, ssl_context=ssl_context)


if __name__ == '__main__':
    main()
