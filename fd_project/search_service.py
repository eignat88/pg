from __future__ import annotations

import argparse
import math

import psycopg2

from .config import AppConfig
from .embeddings import EmbeddingClient


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0

    for x, y in zip(a, b):
        dot += x * y
        norm_a += x * x
        norm_b += y * y

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))


def search_fd(query: str, limit: int = 5, config: AppConfig | None = None) -> list[dict]:
    config = config or AppConfig()
    embedding_client = EmbeddingClient(config.ollama_url, config.ollama_model)
    query_embedding = embedding_client.get_embedding(query)

    conn = psycopg2.connect(**config.db_config)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            c.id,
            d.dax_code,
            d.title,
            c.section_title,
            c.chunk_type,
            c.process_type,
            c.chunk_text,
            c.embedding
        FROM ai.fd_chunks c
        JOIN ai.fd_documents d ON d.id = c.document_id
        WHERE c.embedding IS NOT NULL
        """
    )

    results = []
    for row in cur.fetchall():
        chunk_id, dax_code, title, section_title, chunk_type, process_type, chunk_text, embedding = row
        results.append(
            {
                "score": cosine_similarity(query_embedding, embedding),
                "chunk_id": chunk_id,
                "dax_code": dax_code,
                "title": title,
                "section_title": section_title,
                "chunk_type": chunk_type,
                "process_type": process_type,
                "chunk_text": chunk_text,
            }
        )

    cur.close()
    conn.close()
    return sorted(results, key=lambda x: x["score"], reverse=True)[:limit]


def print_results(results: list[dict]) -> None:
    print("\nТОП найденных фрагментов:\n")
    for i, r in enumerate(results, start=1):
        print("=" * 100)
        print(f"{i}. score: {r['score']:.4f}")
        print(f"ФД: {r['dax_code']} — {r['title']}")
        print(f"Раздел: {r['section_title']}")
        print(f"Тип: {r['chunk_type']} / процесс: {r['process_type']}")
        print(f"Chunk ID: {r['chunk_id']}")
        print("-" * 100)
        print(r["chunk_text"][:2500])
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Поиск по базе знаний ФД")
    parser.add_argument("query", nargs="*", help="Вопрос для поиска")
    parser.add_argument("--limit", type=int, default=5, help="Сколько результатов показать")
    args = parser.parse_args()

    query = " ".join(args.query).strip() or input("Введите вопрос: ").strip()
    if not query:
        print("Вопрос пустой")
        return

    print_results(search_fd(query=query, limit=args.limit))


if __name__ == "__main__":
    main()
