from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TableStats:
    fd_chunks: int
    fd_documents: int
    fd_document_links: int
    fd_entities: int
    fd_chunk_entities: int


class FDRepository:
    def __init__(self, cursor) -> None:
        self.cur = cursor

    def get_table_stats(self) -> TableStats:
        queries = {
            "fd_chunks": "SELECT COUNT(*) FROM ai.fd_chunks",
            "fd_documents": "SELECT COUNT(*) FROM ai.fd_documents",
            "fd_document_links": "SELECT COUNT(*) FROM ai.fd_document_links",
            "fd_entities": "SELECT COUNT(*) FROM ai.fd_entities",
            "fd_chunk_entities": "SELECT COUNT(*) FROM ai.fd_chunk_entities",
        }
        values: dict[str, int] = {}
        for key, sql in queries.items():
            self.cur.execute(sql)
            values[key] = self.cur.fetchone()[0]
        return TableStats(**values)

    def find_document_id_by_source_file(self, source_file: str) -> int | None:
        self.cur.execute("SELECT id FROM ai.fd_documents WHERE source_file = %s LIMIT 1", (source_file,))
        row = self.cur.fetchone()
        return row[0] if row else None

    def delete_document_graph(self, document_id: int) -> None:
        self.cur.execute("SELECT id FROM ai.fd_chunks WHERE document_id = %s", (document_id,))
        chunk_ids = [row[0] for row in self.cur.fetchall()]

        if chunk_ids:
            self.cur.execute("DELETE FROM ai.fd_chunk_entities WHERE chunk_id = ANY(%s)", (chunk_ids,))
            self.cur.execute("DELETE FROM ai.fd_chunks WHERE id = ANY(%s)", (chunk_ids,))

        self.cur.execute(
            "DELETE FROM ai.fd_document_links WHERE source_document_id = %s OR target_document_id = %s",
            (document_id, document_id),
        )
        self.cur.execute("DELETE FROM ai.fd_documents WHERE id = %s", (document_id,))

    def insert_document(self, meta: dict) -> int:
        self.cur.execute(
            """
            INSERT INTO ai.fd_documents
                (title, source_file, dax_code, version, business_process, purpose, author, document_date, source_type)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                meta["title"],
                meta["source_file"],
                meta["dax_code"],
                meta["version"],
                meta["business_process"],
                meta["purpose"],
                meta["author"],
                meta["document_date"],
                meta["source_type"],
            ),
        )
        return self.cur.fetchone()[0]

    def insert_entity(self, name: str) -> int:
        self.cur.execute(
            """
            INSERT INTO ai.fd_entities (name)
            VALUES (%s)
            ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
            RETURNING id
            """,
            (name,),
        )
        return self.cur.fetchone()[0]

    def insert_chunk(self, payload: dict) -> int:
        self.cur.execute(
            """
            INSERT INTO ai.fd_chunks
                (document_id, chunk_text, embedding, section_title, chunk_type, business_terms, jira_keys, process_type)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                payload["document_id"],
                payload["chunk_text"],
                payload["embedding"],
                payload["section_title"],
                payload["chunk_type"],
                payload["business_terms"],
                payload["jira_keys"],
                payload["process_type"],
            ),
        )
        return self.cur.fetchone()[0]

    def link_chunk_entity(self, chunk_id: int, entity_id: int) -> None:
        self.cur.execute(
            """
            INSERT INTO ai.fd_chunk_entities (chunk_id, entity_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
            """,
            (chunk_id, entity_id),
        )

    def insert_document_link(self, source_document_id: int, target_document_id: int, link_type: str = "related") -> None:
        self.cur.execute(
            """
            INSERT INTO ai.fd_document_links (source_document_id, target_document_id, link_type)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (source_document_id, target_document_id, link_type),
        )
