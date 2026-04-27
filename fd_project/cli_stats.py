from __future__ import annotations

from .config import AppConfig
from .db import get_connection
from .repositories import FDRepository


def main() -> None:
    config = AppConfig()
    with get_connection(config) as conn:
        repo = FDRepository(conn.cursor())
        stats = repo.get_table_stats()

    print("ai.fd_chunks\t", stats.fd_chunks)
    print("ai.fd_documents\t", stats.fd_documents)
    print("ai.fd_document_links\t", stats.fd_document_links)
    print("ai.fd_entities\t", stats.fd_entities)
    print("ai.fd_chunk_entities\t", stats.fd_chunk_entities)


if __name__ == "__main__":
    main()
