from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator

import psycopg2

from .config import AppConfig


@contextmanager
def get_connection(config: AppConfig) -> Iterator:
    conn = psycopg2.connect(**config.db_config)
    try:
        yield conn
    finally:
        conn.close()
