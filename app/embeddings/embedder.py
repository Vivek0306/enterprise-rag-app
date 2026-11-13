from docx import text
import ollama

EMBEDDING_MODEL = "bge-m3"
EXPECTED_DIMENSION = 1024

def generate_embedding(texts:  str) -> list[float]:

    embeddings = generate_embeddings([texts])
    return embeddings[0]


def generate_embeddings(texts:  list[str]) -> list[list[float]]:

    if not texts:
        return []
    print(texts)
    if any(not text or not text.strip() for text in texts):
        raise ValueError("Cannot embed empty text.")

    response = ollama.embed(
        model = EMBEDDING_MODEL,
        input = texts
    )

    embeddings = response["embeddings"]

    if len(embeddings) != len(texts):
        raise ValueError("Embedding count does not match input count.")

    for embedding in embeddings:
        if len(embedding) != EXPECTED_DIMENSION:
            raise ValueError(
                f"Expected {EXPECTED_DIMENSION} dimensions, recevied {len(embedding)}"
            )

    return embeddings