import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from application.main import init_app
from application.settings import BASE_DIR, get_config
from init_db import (create_tables, drop_tables, sample_data, setup_db,
                     teardown_db)

TEST_CONFIG_PATH = BASE_DIR / 'config' / 'demo_test.yaml'
TEST_CONFIG = get_config(TEST_CONFIG_PATH)
TEST_DB_URL = (
    'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'.format(
        **TEST_CONFIG['postgres'],
    )
)


@pytest.fixture
async def client(aiohttp_client, db):
    """Создание приложения и тестового клиента."""
    app = await init_app()
    return await aiohttp_client(app)


@pytest.fixture(scope='module')
async def db():
    """Создание тестовой базы и пользователя, удаление по завершению тестов."""
    await setup_db(TEST_CONFIG)
    yield
    await teardown_db(TEST_CONFIG)


@pytest.fixture
async def tables_and_data():
    """Создание таблицы и наполнение их данными."""
    test_engine = create_async_engine(TEST_DB_URL)
    await create_tables(test_engine)
    await sample_data(test_engine)
    yield
    await drop_tables(test_engine)
