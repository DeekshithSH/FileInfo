from os import environ
import pathlib
from dotenv import load_dotenv

load_dotenv(".env")

class Var(object):
    PORT=int(environ.get("PORT", None))
    DEBUG=str(environ.get("DEBUG", "0").lower()) in ("1", "true", "t", "yes", "y")
    BIND_ADDRESS="0.0.0.0"
    PROJECT_PATH = pathlib.Path(__file__).parent