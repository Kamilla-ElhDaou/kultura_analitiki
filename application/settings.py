import pathlib

import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config' / 'demo.yaml'


def get_config(path):
    """Получение конфигурационных данных из yaml."""
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


config = get_config(config_path)

DSN = 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'
