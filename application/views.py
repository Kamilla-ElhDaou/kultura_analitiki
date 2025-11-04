from aiohttp.web import View, json_response

from application.db import (ObjectDoesAlreadyExist, ObjectDoesNotExist,
                            create_author, create_book, get_author, get_book)
from application.typedefs import db_key


class AuthorDetailView(View):
    """Вью для получения автора.."""

    async def get(self):
        """
        Получить книгу по id.
        ---
        summary: Информация о конкретном авторе
        tags:
          - Author

        parameters:
          - name: author_id
            in: path
            required: true
            description: id автора
            schema:
              type: integer

        responses:
          '200':
            description: Успешно
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    author:
                      type: object
                      properties:
                        first_name: { type: string }
                        last_name: { type: string }
                        books:
                          type: array
                          items:
                            type: string
          '404':
            description: Автор не найден
        """

        async with self.request.app[db_key]() as sess:
            author_id = int(self.request.match_info['author_id'])
            try:
                response = await get_author(sess, author_id)
            except ObjectDoesNotExist as e:
                return json_response({'error': str(e)}, status=404)

            return json_response({'author': response, }, status=200)


class AuthorCreateView(View):
    """Вью для создания автора.."""

    async def post(self):
        """
        Создать нового автора.
        ---
        summary: Создание автора

        tags:
          - Author

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - first_name
                  - last_name
                properties:
                  first_name: { type: string }
                  last_name: { type: string }

        responses:
          '201':
            description: Создано
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    author:
                      type: object
                      properties:
                        first_name: { type: string }
                        last_name: { type: string }
                        books:
                          type: array
                          items:
                            type: string
          '400':
            description: Автор уже существует
        """

        async with self.request.app[db_key].begin() as sess:
            data = await self.request.json()
            try:
                response = await create_author(sess, data=data)
            except ObjectDoesAlreadyExist as e:
                return json_response({'error': str(e)}, status=400)

            return json_response({'author': response, }, status=201)


class BookDetailView(View):
    """Вью для получения книги."""

    async def get(self):
        """
        Получить книгу по id.
        ---
        summary: Информация о конкретной книги
        tags:
          - Books

        parameters:
          - name: book_id
            in: path
            required: true
            description: id книги
            schema:
              type: integer

        responses:
          '200':
            description: Успешно
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    book:
                      type: object
                      properties:
                        id: { type: integer }
                        title: { type: string }
                        author: { type: string }
          '404':
            description: Книга не найдена
        """

        async with self.request.app[db_key]() as sess:
            book_id = int(self.request.match_info['book_id'])
            try:
                response = await get_book(sess, book_id)
            except ObjectDoesNotExist as e:
                return json_response({'error': str(e)}, status=404)

            return json_response({'book': response, }, status=200)


class BookCreateView(View):
    """Вью для создания книги."""

    async def post(self):
        """
        Создать новую книгу.
        ---
        summary: Создание книги

        tags:
          - Books

        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                required:
                  - title
                  - author_id
                properties:
                  title: { type: string }
                  author: { type: integer }

        responses:
          '201':
            description: Создано
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    book:
                      type: object
                      properties:
                        id: { type: integer }
                        title: { type: string }
                        author: { type: string }
          '400':
            description: Автор книги не найден
        """

        async with self.request.app[db_key].begin() as sess:
            data = await self.request.json()
            try:
                response = await create_book(sess, data=data)
            except ObjectDoesNotExist as e:
                return json_response({'error': str(e)}, status=400)

            return json_response({'book': response, }, status=201)
