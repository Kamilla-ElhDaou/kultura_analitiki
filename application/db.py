from typing import List

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import (DeclarativeBase, Mapped, joinedload, mapped_column,
                            relationship, selectinload)

from application.settings import DSN
from application.typedefs import config_key, db_key


class Base(DeclarativeBase):
    """Базлвый класс для моделей приложения."""


class Author(Base):
    """Модель автора."""

    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    books: Mapped[List['Book']] = relationship(back_populates='author')

    def to_dict(self, books=False):
        """Преобразование данных в словарь."""
        if books:
            data = [book.title for book in self.books]
        else:
            data = []
        return dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            books=data,
        )


class Book(Base):
    """Модель книги."""

    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    author_id: Mapped[int] = mapped_column(
        ForeignKey('author.id', ondelete='CASCADE')
    )
    author: Mapped['Author'] = relationship(back_populates='books')

    def to_dict(self):
        """Преобразование данных в словарь."""
        return dict(
            id=self.id,
            title=self.title,
            author=f'{self.author.first_name} {self.author.last_name}',
        )


class ObjectDoesNotExist(Exception):
    """Объект в базе данных не найден."""


class ObjectDoesAlreadyExist(Exception):
    """Объект в базе данных уже существует."""


async def pg_context(app):
    engine = create_async_engine(DSN.format(**app[config_key]['postgres'],))

    app[db_key] = async_sessionmaker(engine)

    yield

    await engine.dispose()


async def get_author(sess, author_id):
    """Получение автора."""
    result = await sess.scalars(
        select(
            Author
        ).where(
            Author.id == author_id
        ).options(
            selectinload(Author.books)
        )
    )
    author = result.first()

    if not author:
        raise ObjectDoesNotExist(f'Автор {author_id} не найден.')

    return author.to_dict(books=True)


async def create_author(sess, data):
    """Создание автора."""
    result = await sess.scalars(
        select(
            Author
        ).where(
            Author.first_name == data['first_name']
        ).where(
            Author.last_name == data['last_name']
        )
    )

    if result.first():
        raise ObjectDoesAlreadyExist

    author = Author(**data)
    sess.add(author)
    await sess.flush()

    return author.to_dict()


async def get_book(sess, book_id):
    """Получение книги."""
    result = await sess.scalars(
        select(
            Book
        ).where(
            Book.id == book_id
        ).options(
            joinedload(Book.author)
        )
    )
    book = result.first()

    if not book:
        raise ObjectDoesNotExist(f'Книга {book_id} не найдена.')

    return book.to_dict()


async def create_book(sess, data):
    """Создание книги."""
    author_id = data.get('author_id')
    if author_id:
        author = await sess.get(Author, author_id)
        if not author:
            raise ObjectDoesNotExist(f'Автор {author_id} не найден.')

        book = Book(**data)
        sess.add(book)
        await sess.flush()

        return book.to_dict()
