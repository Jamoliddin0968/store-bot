import json

from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse(content={"dsf": "dsf"})

app = Starlette(debug=True, routes=[
    Route('/', homepage),
])
