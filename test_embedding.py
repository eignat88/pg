import requests

def get_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    return response.json()["embedding"]

text = "подбирать партии без маркировки"

embedding = get_embedding(text)

print(len(embedding))