# coding: utf-8

import pytest
import json
from aiohttp import web

from openapi_server.models.book_book_id_get200_response import BookBookIdGet200Response
from openapi_server.models.book_post_request import BookPostRequest


pytestmark = pytest.mark.asyncio

async def test_book_book_id_get(client):
    """Test case for book_book_id_get

    Информация о конкретной книги
    """
    headers = { 
        'Accept': 'application/json',
    }
    response = await client.request(
        method='GET',
        path='/book/{book_id}'.format(book_id=56),
        headers=headers,
        )
    assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


pytestmark = pytest.mark.asyncio

async def test_book_post(client):
    """Test case for book_post

    Создание книги
    """
    body = openapi_server.BookPostRequest()
    headers = { 
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = await client.request(
        method='POST',
        path='/book',
        headers=headers,
        json=body,
        )
    assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')

