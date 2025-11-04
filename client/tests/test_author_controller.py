# coding: utf-8

import pytest
import json
from aiohttp import web

from openapi_server.models.author_author_id_get200_response import AuthorAuthorIdGet200Response
from openapi_server.models.author_post_request import AuthorPostRequest


pytestmark = pytest.mark.asyncio

async def test_author_author_id_get(client):
    """Test case for author_author_id_get

    Информация о конкретном авторе
    """
    headers = { 
        'Accept': 'application/json',
    }
    response = await client.request(
        method='GET',
        path='/author/{author_id}'.format(author_id=56),
        headers=headers,
        )
    assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')


pytestmark = pytest.mark.asyncio

async def test_author_post(client):
    """Test case for author_post

    Создание автора
    """
    body = openapi_server.AuthorPostRequest()
    headers = { 
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = await client.request(
        method='POST',
        path='/author',
        headers=headers,
        json=body,
        )
    assert response.status == 200, 'Response body is : ' + (await response.read()).decode('utf-8')

