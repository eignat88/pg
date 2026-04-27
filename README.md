# fd-project

Проект для загрузки функциональных документов (`.docx`) в PostgreSQL и семантического поиска по ним.

## Актуальная модель БД

Код ориентирован на следующие таблицы в схеме `ai`:
- `fd_chunks`
- `fd_documents`
- `fd_document_links`
- `fd_entities`
- `fd_chunk_entities`

Добавлена отдельная CLI-команда для проверки фактических количеств строк в этих таблицах.

## Структура

- `fd_project/config.py` — конфигурация через env-переменные;
- `fd_project/db.py` — подключение к PostgreSQL;
- `fd_project/repositories.py` — операции с таблицами `ai.fd_*`;
- `fd_project/loader_service.py` — чтение DOCX, чанкование, загрузка и пересборка связей;
- `fd_project/search_service.py` — семантический поиск с подгрузкой entities и связанных документов;
- `fd_project/cli_load_docx.py` — CLI загрузки DOCX;
- `fd_project/cli_stats.py` — CLI статистики по таблицам.

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

### Проверка размеров таблиц

```bash
fd-db-stats
```

### Загрузка DOCX

```bash
fd-load-docx --docx-folder ./docs
```

По умолчанию загрузка работает в режиме *replace* по `source_file`: если документ с таким именем уже есть,
он удаляется вместе с зависимыми chunk/link-связями и загружается заново.

Чтобы отключить replace-поведение:

```bash
fd-load-docx --docx-folder ./docs --no-replace
```

### Поиск

```bash
fd-search "подбирать партии без маркировки" --limit 5
```

Вывод включает score, chunk, entities и связанные document id.

## Backward compatibility

Старые скрипты оставлены как thin wrappers:
- `load_fd_docx.py`
- `search.py`
- `test_embedding.py`
