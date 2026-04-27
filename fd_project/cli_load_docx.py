from __future__ import annotations

import argparse
from pathlib import Path

from .config import AppConfig
from .loader_service import load_docx_batch


def main() -> None:
    parser = argparse.ArgumentParser(description="Загрузка FD DOCX в PostgreSQL")
    parser.add_argument("--docx-folder", type=Path, default=None, help="Папка с .docx файлами")
    parser.add_argument(
        "--no-replace",
        action="store_true",
        help="Не удалять ранее загруженный документ с таким же source_file",
    )
    args = parser.parse_args()

    config = AppConfig(docx_folder=args.docx_folder) if args.docx_folder else AppConfig()
    load_docx_batch(config, replace_existing=not args.no_replace)


if __name__ == "__main__":
    main()
