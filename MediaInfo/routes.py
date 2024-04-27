import ffmpeg
from aiohttp import web

from MediaInfo.vars import Var

routes = web.RouteTableDef()

@routes.post("/api")
async def root_route_handler(request: web.Request):
    pass

app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app)
