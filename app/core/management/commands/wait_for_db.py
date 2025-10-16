"""
Django command to wait for the database to be available.
"""
import time
from typing import Any

from psycopg.errors import OperationalError as PsycopgOpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

from app.logger_config import setup_logger


logger = setup_logger(__name__)


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args: Any, **options: Any) -> None:
        logger.info("Waiting for database to become available...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (PsycopgOpError, OperationalError):
                logger.warning("Database unavailable, retrying in 1 second...")
                time.sleep(1)

        logger.info("Database is now available!")
