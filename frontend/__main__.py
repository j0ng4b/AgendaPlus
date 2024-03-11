from dotenv import load_dotenv
import flet

from . import main


load_dotenv('.env.shared')
load_dotenv('.env.frontend')

# Run front-end
flet.app(target=main)
