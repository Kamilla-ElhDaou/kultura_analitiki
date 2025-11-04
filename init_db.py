import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from application.db import Author, Base, Book
from application.settings import BASE_DIR, DSN, config, get_config

config_path = BASE_DIR / 'config' / 'demo_init.yaml'
init_config = get_config(config_path)

DSN_INIT = DSN.format(**init_config['postgres'],)

init_engine = create_async_engine(DSN_INIT, isolation_level='AUTOCOMMIT')

app_engine = create_async_engine(
    DSN.format(**config['postgres'],
               isolation_level='AUTOCOMMIT')
)


async def setup_db(config):
    """Создает базу данных, пользователя и предоставляет ему права."""
    db_name = config['postgres']['database']
    db_user = config['postgres']['user']
    db_pass = config['postgres']['password']

    async with init_engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
        await conn.execute(
            text(f"CREATE USER {db_user} WITH PASSWORD '{db_pass}'")
        )
        await conn.execute(text(f"CREATE DATABASE {db_name} ENCODING 'UTF8'"))
        await conn.execute(text(
            f"ALTER DATABASE {db_name} OWNER TO {db_user}"
        ))
        await conn.execute(text(f"GRANT ALL ON SCHEMA public TO {db_user}"))
        await conn.commit()


async def teardown_db(config):
    """Завершает все подключения, удаляет базу данных и пользователей."""
    db_name = config['postgres']['database']
    db_user = config['postgres']['user']

    async with init_engine.connect() as conn:
        await conn.execute(
            text(
                "SELECT pg_terminate_backend(pg_stat_activity.pid) "
                "FROM pg_stat_activity "
                f"WHERE pg_stat_activity.datname = '{db_name}' "
                "AND pid <> pg_backend_pid();"
            )
        )
        await conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))
        await conn.execute(text(f"REVOKE ALL ON SCHEMA public FROM {db_user}"))
        await conn.execute(text(f"DROP ROLE IF EXISTS {db_user}"))
        await conn.commit()


async def create_tables(engine):
    """Создает все таблицы в базе."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def drop_tables(engine):
    """Удаляет все таблицы из базы."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


async def sample_data(engine):
    """Заполняет базу данных данными."""
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session.begin() as sess:
        sess.add_all(
            (
                Author(first_name='Александр', last_name='Пушкин'),
                Author(first_name='Михаил', last_name='Лермонтов'),
                Author(first_name='Лев ', last_name='Толстой'),
            )
        )
    async with Session.begin() as sess:
        sess.add_all(
            (
                Book(title='Капитанская дочка', author_id=1),
                Book(title='Евгений Онегин', author_id=1),
                Book(title='Борис Годунов', author_id=1),
                Book(title='Герой нашего времени', author_id=2),
                Book(title='Бородино', author_id=2),
                Book(title='Смерть поэта', author_id=2),
                Book(title='Война и мир', author_id=3),
                Book(title='Анна Каренина', author_id=3),
                Book(title='Кавказский пленик', author_id=3),

            )
        )


if __name__ == '__main__':
    asyncio.run(setup_db(config))
    asyncio.run(create_tables(engine=app_engine))
    asyncio.run(sample_data(engine=app_engine))
