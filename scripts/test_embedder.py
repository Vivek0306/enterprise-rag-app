
from app.embeddings.embedder import generate_embeddings

sample_texts = [
    "Employees receive annual leave.",
    "Managers approve employee leave requests.",
    "The company provides medical insurance.",
]

embeddings = generate_embeddings(sample_texts)

print("Number of embeddings:", len(embeddings))

for index, embedding in enumerate(embeddings):
    print(f"Chunk {index}: {len(embedding)} dimensions")
    print("First five values:", embedding[:5])
