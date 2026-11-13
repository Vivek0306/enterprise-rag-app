
SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'document_chunks';


SELECT
    vector_dims(embedding) AS dimensions,
    COUNT(*) AS chunks
FROM document_chunks
WHERE embedding IS NOT NULL
GROUP BY vector_dims(embedding);



CREATE INDEX ix_document_chunks_embedding_hnsw
ON document_chunks
USING hnsw (embedding vector_cosine_ops);


ALTER TABLE document_chunks
ADD COLUMN content_tsv tsvector
GENERATED ALWAYS AS (
    to_tsvector('english', coalesce(content, ''))
) STORED;


CREATE INDEX ix_document_chunks_content_tsv
ON document_chunks
USING GIN (content_tsv);



SELECT
    chunk_index,
    content,
    content_tsv
FROM document_chunks
LIMIT 5;



SELECT
    chunk_index,
    content,
    ts_rank(
        content_tsv,
        websearch_to_tsquery('english', 'annual leave')
    ) AS relevance
FROM document_chunks
WHERE content_tsv @@
      websearch_to_tsquery('english', 'annual leave')
ORDER BY relevance DESC;