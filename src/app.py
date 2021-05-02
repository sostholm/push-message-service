from re import L
from starlette.applications     import Starlette
from starlette.responses        import Response
from starlette.routing          import Route
from starlette.requests         import Request
from starlette.middleware       import Middleware
from starlette.middleware.cors  import CORSMiddleware

import uvicorn

from web_push import send_web_push


async def web_push(request: Request):
    body = await request.json()
    assert 'subscription' in body
    assert 'text' in body
    
    send_web_push(body['subscription'], body['text'])

    return Response()


routes = [
    Route('/web-push', web_push, methods=['POST'])
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

app = Starlette(routes=routes)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9000)
