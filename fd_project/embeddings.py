from __future__ import annotations

import requests


class EmbeddingClient:
    def __init__(self, url: str, model: str) -> None:
        self.url = url
        self.model = model

    def get_embedding(self, text: str) -> list[float]:
        response = requests.post(
            self.url,
            json={"model": self.model, "prompt": text},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["embedding"]
