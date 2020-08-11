import os
from pathlib import Path
from typing import Optional


class TestConfig:
    """
    Test config
    """

    ROOT_DIR: Path = Path(__file__).parent.parent
    SECRET_KEY: Optional[str] = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATION_DIR: str = os.path.join(ROOT_DIR, "database", "migrations")
    BASIC_AUTH_USERNAME = os.environ.get("ADMIN")
    BASIC_AUTH_PASSWORD = os.environ.get("PASSWORD")


config = TestConfig()
