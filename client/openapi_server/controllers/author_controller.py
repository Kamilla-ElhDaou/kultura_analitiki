from typing import List, Dict
from aiohttp import web

from openapi_server.models.author_author_id_get200_response import AuthorAuthorIdGet200Response
from openapi_server.models.author_post_request import AuthorPostRequest
from openapi_server import util


async def author_author_id_get(request: web.Request, author_id) -> web.Response:
    """Информация о конкретном авторе

    

    :param author_id: id автора
    :type author_id: int

    """
    return web.Response(status=200)


async def author_post(request: web.Request, body) -> web.Response:
    """Создание автора

    

    :param body: 
    :type body: dict | bytes

    """
    body = AuthorPostRequest.from_dict(body)
    return web.Response(status=200)
