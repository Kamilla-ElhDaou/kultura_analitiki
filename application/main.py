import sys

from aiohttp import web
from aiohttp_swagger3 import SwaggerDocs, SwaggerInfo, SwaggerUiSettings

from application.db import pg_context
from application.settings import config
from application.typedefs import config_key
from application.views import (AuthorCreateView, AuthorDetailView,
                               BookCreateView, BookDetailView)


async def init_app(argv=None):
    """Создание приложения и регистрация маршрутов."""
    app = web.Application()
    swagger = SwaggerDocs(
        app,
        swagger_ui_settings=SwaggerUiSettings(path='/docs/'),
        info=SwaggerInfo(
            title='Swagger Demo',
            version='1.0.0',
            description='API для управления авторами и их книгами',
        ),
    )
    swagger.add_routes([
        web.view('/author/{author_id}', AuthorDetailView, name='author_get'),
        web.view('/author', AuthorCreateView, name='author_create'),
        web.view('/book/{book_id}', BookDetailView, name='book_get'),
        web.view('/book', BookCreateView, name='book_create'),
    ])
    app[config_key] = config
    app.cleanup_ctx.append(pg_context)

    return app


def main(argv):
    """Запуск приложения."""
    app = init_app(argv)

    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
