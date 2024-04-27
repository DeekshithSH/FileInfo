
import asyncio
import logging
import sys
import traceback

from aiohttp import web

from MediaInfo.vars import Var
from MediaInfo.app import web_server
print(Var.PROJECT_PATH)

logging.basicConfig(
    level=logging.DEBUG if Var.DEBUG else logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="[%(asctime)s][%(name)s][%(levelname)s] ==> %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout),
              logging.FileHandler("MediaInfo.log", mode="a", encoding="utf-8")],)

logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

loop=asyncio.new_event_loop()

server = web.AppRunner(web_server())

def main() -> None:
    loop.run_until_complete(server.setup())
    site = web.TCPSite(
        server,
        host=Var.BIND_ADDRESS,
        port=Var.PORT,
    )
    loop.run_until_complete(site.start())
    names = sorted(str(s.name) for s in server.sites)
    print(
        "======== Running on {} ========\n"
        "(Press CTRL+C to quit)".format(", ".join(names))
    )
    loop.run_forever()

async def cleanup():
    await server.cleanup()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        traceback.print_exc()
    finally:
        loop.run_until_complete(cleanup())
        loop.close()
        print("Server Stoped")