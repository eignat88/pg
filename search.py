import argparse
import math
import requests
import psycopg2


DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432",
}

OLLAMA_URL = "http://localhost:11434/api/embeddings"
OLLAMA_MODEL = "nomic-embed-text"


def get_embedding(text: str) -> list[float]:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": text,
        },
        timeout=120,
    )
    response.raise_for_status()
    return response.json()["embedding"]


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


def search_fd(query: str, limit: int = 5):
    query_embedding = get_embedding(query)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
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
    """)

    rows = cur.fetchall()

    results = []

    for row in rows:
        chunk_id, dax_code, title, section_title, chunk_type, process_type, chunk_text, embedding = row
        score = cosine_similarity(query_embedding, embedding)

        results.append({
            "score": score,
            "chunk_id": chunk_id,
            "dax_code": dax_code,
            "title": title,
            "section_title": section_title,
            "chunk_type": chunk_type,
            "process_type": process_type,
            "chunk_text": chunk_text,
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    cur.close()
    conn.close()

    return results[:limit]


def print_results(results):
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


def main():
    parser = argparse.ArgumentParser(description="Поиск по базе знаний ФД")
    parser.add_argument("query", nargs="*", help="Вопрос для поиска")
    parser.add_argument("--limit", type=int, default=5, help="Сколько результатов показать")

    args = parser.parse_args()

    query = " ".join(args.query).strip()

    if not query:
        query = input("Введите вопрос: ").strip()

    if not query:
        print("Вопрос пустой")
        return

    results = search_fd(query=query, limit=args.limit)
    print_results(results)


if __name__ == "__main__":
    main()