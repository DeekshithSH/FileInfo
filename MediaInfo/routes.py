import os

from aiohttp import web
from bson import ObjectId

from MediaInfo.utils.file import get_metadata
from MediaInfo.vars import Var

routes = web.RouteTableDef()

@routes.post("/api")
async def root_route_handler(request: web.Request):
    reader = await request.multipart()
    field = await reader.next()
    filepath = f"{Var.PROJECT_PATH}/uploads/{ObjectId()}"
    # Open a new file with write-binary mode
    
    with open(filepath, 'wb') as f:
        # Iterate over the field content by chunks
        while True:
            chunk = await field.read_chunk()  # Read 64KB chunks of the field's content
            if not chunk:
                break
            # Write the chunk to the file
            f.write(chunk)

    resp=get_metadata(filepath)
    os.remove(filepath)
    
    return web.Response(text=resp)

app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app)
