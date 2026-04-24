from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class AppConfig:
    dbname: str = os.getenv("PG_DBNAME", "postgres")
    user: str = os.getenv("PG_USER", "postgres")
    password: str = os.getenv("PG_PASSWORD", "123")
    host: str = os.getenv("PG_HOST", "localhost")
    port: str = os.getenv("PG_PORT", "5432")
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/embeddings")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "nomic-embed-text")
    docx_folder: Path = Path(os.getenv("DOCX_FOLDER", str(Path.cwd() / "docs")))

    @property
    def db_config(self) -> dict[str, str]:
        return {
            "dbname": self.dbname,
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "port": self.port,
        }
