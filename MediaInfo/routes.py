import os

from aiohttp import web, ClientSession, ClientTimeout
from aiohttp.client_exceptions import InvalidURL
from asyncio.exceptions import TimeoutError
from bson import ObjectId

from MediaInfo.utils.file import get_metadata
from MediaInfo.vars import Var

routes = web.RouteTableDef()

@routes.post("/api/file")
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

@routes.post("/api/url")
async def root_route_handler(request: web.Request):
    filepath = f"{Var.PROJECT_PATH}/uploads/{ObjectId()}"
    url = (await request.read()).decode()
    try:
        async with ClientSession(timeout=ClientTimeout(total=60)) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    chunk_size = 1024 * 1024
                    data = bytearray()
                    while len(data) < 2 * 1024 * 1024:
                        chunk = await resp.content.read(chunk_size)
                        if not chunk:
                            break
                        data.extend(chunk)
                    
                    # Write the data to a file
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    
                    resp_text = get_metadata(filepath)
                    os.remove(filepath)
                else:
                    resp_text = f"Error: Received status code {resp.status} from URL"
    except InvalidURL as e:
        resp_text = f"InvalidURL: {e}"
    except TimeoutError:
        resp_text = f"TimeOut: couldn't fetch file withon 1 minute"
    except Exception as e:
        resp_text = f"Error: {e}"
    
    return web.Response(text=resp_text)