import yaml
from pathlib import Path

# Корень проекта
BASE_DIR = Path(__file__).resolve().parent

# Подгружаем конфиг
CONFIG_FILE_PATH = Path(BASE_DIR, 'config.yml')
_raw_config = CONFIG_FILE_PATH.read_text(encoding='utf-8')
_config = yaml.load(_raw_config, yaml.Loader)


class Config:
    # Системные настройки
    SECRET_KEY: str = _config['SECRET_KEY']
    DEBUG: bool = _config['DEBUG']

    # База данных
    SQLITE_DB_NAME = _config['SQLITE_DB_NAME']
    DATABASE = {
        'name': SQLITE_DB_NAME,
        'engine': 'peewee.SqliteDatabase',
    }

    # Данные для входа админа
    ADMIN_USERNAME: str = _config['ADMIN_USERNAME']
    ADMIN_PASSWORD: str = _config['ADMIN_PASSWORD']

    # Другие настройки
    TASKS_ON_PAGE: int = _config['TASKS_ON_PAGE']
    CORS_SUPPORTS_CREDENTIALS = True
