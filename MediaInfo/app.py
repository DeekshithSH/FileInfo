import logging
import pathlib
from aiohttp import web
from .routes import routes
from MediaInfo.vars import Var

logger = logging.getLogger("server")

def web_server():
    web_app = web.Application()
    web_app.add_routes(routes)

    # added static dir
    web_app.router.add_static(
        '/',
        path=(Var.PROJECT_PATH / 'static'),
        name='static',
    )
    return web_app