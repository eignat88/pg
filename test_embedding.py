from fd_project.config import AppConfig
from fd_project.embeddings import EmbeddingClient


if __name__ == "__main__":
    config = AppConfig()
    embedding = EmbeddingClient(config.ollama_url, config.ollama_model).get_embedding(
        "подбирать партии без маркировки"
    )
    print(len(embedding))
