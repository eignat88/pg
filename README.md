# fd-project

Небольшой Python-проект для:
- загрузки функциональных документов (`.docx`) в PostgreSQL;
- построения embedding через Ollama;
- семантического поиска по загруженным фрагментам.

## Структура

- `fd_project/config.py` — централизованная конфигурация через env-переменные;
- `fd_project/embeddings.py` — клиент для Ollama embeddings API;
- `fd_project/loader_service.py` — обработка DOCX и загрузка в БД;
- `fd_project/search_service.py` — семантический поиск по chunk-ам;
- `fd_project/cli_load_docx.py` — CLI для загрузки документов.

Совместимость сохранена:
- `load_fd_docx.py` и `search.py` оставлены как тонкие wrappers.

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Конфигурация (env)

- `PG_DBNAME` (default: `postgres`)
- `PG_USER` (default: `postgres`)
- `PG_PASSWORD` (default: `123`)
- `PG_HOST` (default: `localhost`)
- `PG_PORT` (default: `5432`)
- `OLLAMA_URL` (default: `http://localhost:11434/api/embeddings`)
- `OLLAMA_MODEL` (default: `nomic-embed-text`)
- `DOCX_FOLDER` (default: `./docs`)

## Использование

### Загрузка DOCX

```bash
fd-load-docx --docx-folder ./docs
```

или

```bash
python load_fd_docx.py --docx-folder ./docs
```

### Поиск

```bash
fd-search "подбирать партии без маркировки" --limit 5
```

или

```bash
python search.py "подбирать партии без маркировки" --limit 5
```
