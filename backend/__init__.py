import importlib
import os
import os.path
from typing import Dict, Any, cast

from dotenv import dotenv_values
from flask import Flask, Blueprint


def create_app(config: Dict[str, Any]) -> Flask:
    app = Flask(__name__.split('.')[0], instance_relative_config=True)

    # Load configurations
    app.config.from_mapping(config)

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

    di[IUserService] = di[UserService]


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
    config = {
        **dotenv_values('.env.backend')
    }

    app = create_app(config)
    app.run(port=cast(int, config.get('SERVER_PORT', 5000)), debug=True)


if __name__ == '__main__':
    main()
