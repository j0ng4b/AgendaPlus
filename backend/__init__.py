import importlib
import os
import os.path
from typing import Optional, Dict, Any, cast

from dotenv import load_dotenv
from flask import Flask, Blueprint


def create_app(test_config: Optional[Dict[str, Any]] = None) -> Flask:
    app = Flask(__name__.split('.')[0], instance_relative_config=True)

    # Load configurations
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Create instance directory
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    # Bootstrap
    bootstrap_di(app)
    bootstrap_blueprints(app)

    return app


def bootstrap_di(app: Flask) -> None:
    from kink import di

    # Unit of work
    from .unit_of_work import IUnitOfWork, UnitOfWorkInMemory

    di[IUnitOfWork] = UnitOfWorkInMemory()

    # Services
    from .services.user import IUserService, UserService
    from .services.refresh_token import IRefreshTokenService, \
        RefreshTokenService

    di[IUserService] = di[UserService]
    di[IRefreshTokenService] = di[RefreshTokenService]


def bootstrap_blueprints(app: Flask) -> None:
    api = Blueprint('api', __name__)

    blueprints_root = os.path.join(app.root_path, 'blueprints')
    for blueprint_file in os.listdir(blueprints_root):
        if blueprint_file.startswith('__') \
                or not blueprint_file.endswith('.py'):
            continue

        # Removes .py extension
        blueprint_name = blueprint_file.strip('.py')

        # Dynamic import the route blueprint
        blueprint_module_name = f'.blueprints.{blueprint_name}'
        blueprint_module = importlib.import_module(blueprint_module_name,
                                                   __package__)

        blueprint_name += '_bp'
        if blueprint_name in blueprint_module.__dict__:
            # Try to register the blueprint <blueprint_name>_bp
            api.register_blueprint(blueprint_module.__dict__[blueprint_name])
        else:
            print(f'Blueprint {blueprint_name} for {blueprint_module_name}'
                  f'not found!')

    app.register_blueprint(api, url_prefix='/api')


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
