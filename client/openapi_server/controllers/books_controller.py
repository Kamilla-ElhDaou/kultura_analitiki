from typing import List, Dict
from aiohttp import web

from openapi_server.models.book_book_id_get200_response import BookBookIdGet200Response
from openapi_server.models.book_post_request import BookPostRequest
from openapi_server import util


async def book_book_id_get(request: web.Request, book_id) -> web.Response:
    """Информация о конкретной книги

    

    :param book_id: id книги
    :type book_id: int

    """
    return web.Response(status=200)


async def book_post(request: web.Request, body) -> web.Response:
    """Создание книги

    

    :param body: 
    :type body: dict | bytes

    """
    body = BookPostRequest.from_dict(body)
    return web.Response(status=200)
