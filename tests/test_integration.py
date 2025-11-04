import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'url, data, status',
    (
        (
            '/author/1',
            {
                'id': 1,
                'first_name': 'Александр',
                'last_name': 'Пушкин',
                'books': [
                    'Капитанская дочка',
                    'Евгений Онегин',
                    'Борис Годунов',
                ]
            },
            200
        ),
        (
            '/book/1',
            {'title': 'Капитанская дочка', 'author': 'Александр Пушкин'},
            200
        )
    )
)
async def test_get_routes_available(client, tables_and_data, url, data, status):
    """Проверяет доступность адресов get-запросов."""
    async with client.get(url) as response:
        assert response.status == status
        json_data = await response.json()

        key = 'author' if 'author' in url else 'book'
        obj = json_data[key]

        for key, value in data.items():
            assert obj[key] == value


@pytest.mark.parametrize(
    'url, status',
    (
        ('/author/404', 404), ('/book/404', 404)
    )
)
async def test_get_routes_not_available(client, tables_and_data, url, status):
    """Проверяет недоступность адресов get-запросов."""
    async with client.get(url) as response:
        assert response.status == status


@pytest.mark.parametrize(
    'url, data, status',
    (
        ('/author',
         {'first_name': 'Иван', 'last_name': 'Тургенев'},
         201),
    )
)
async def test_create_author_and_book(client, tables_and_data, url, data,
                                      status):
    """Создаёт автора, затем книгу, связанную с ним."""

    author_resp = await client.post(url, json=data)
    assert author_resp.status == status

    author_json = await author_resp.json()
    created_author = author_json['author']

    for key, value in data.items():
        assert created_author[key] == value
    assert created_author['books'] == []

    book_data = {'title': 'Отцы и дети', 'author_id': created_author['id']}
    book_resp = await client.post('/book', json=book_data)
    assert book_resp.status == 201

    book_json = await book_resp.json()
    created_book = book_json['book']

    assert created_book['title'] == 'Отцы и дети'
    assert created_book['author'] == (
        f'{created_author["first_name"]} {created_author["last_name"]}'
    )

    author_check_resp = await client.get(f'/author/{created_author["id"]}')
    assert author_check_resp.status == 200
    author_check_json = await author_check_resp.json()
    author_data = author_check_json['author']

    assert created_book['title'] in author_data['books']


@pytest.mark.parametrize(
    'url, data, status',
    (
        ('/author',
         {'first_name': 'Иван', 'last_name': 'Тургенев'},
         400),
    )
)
async def test_create_author_again(client, tables_and_data, url, data, status):
    """Создаёт дубль автора."""

    author_resp = await client.post(url, json=data)
    assert author_resp.status == status
