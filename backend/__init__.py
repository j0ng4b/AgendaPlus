import importlib
import os
import os.path
from typing import Optional, Dict

from dotenv import load_dotenv
from flask import Flask


def create_app(test_config: Optional[Dict[str, int]] = None) -> Flask:
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

    # Bootstrap blueprints
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
            app.register_blueprint(blueprint_module.__dict__[blueprint_name])
        else:
            print(f'Blueprint {blueprint_name} for {blueprint_module_name}'
                  f'not found!')

    return app


def main() -> None:
    DEFAULT_SERVER_PORT = 5000

    # Load environment variables from .env file
    load_dotenv()

    # Setup variables from environment
    SERVER_PORT = os.getenv('SERVER_PORT', default=DEFAULT_SERVER_PORT)

    app = create_app()
    app.run(port=SERVER_PORT, debug=True)


if __name__ == '__main__':
    main()
