import os

from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

_CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config():
    env = os.environ.get("FLASK_ENV", "development")
    return _CONFIG_MAP.get(env, DevelopmentConfig)
