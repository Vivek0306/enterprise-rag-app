from app.ingestion.extractor import ExtractedPage
from app.ingestion.chunker import chunk_pages


sample_text = """
Company Leave Policy

Employees are entitled to 20 days of annual paid leave.

Employees must submit leave requests five working days
before the planned leave date.

Managers are responsible for reviewing leave requests
within two working days.

Employees are entitled to 10 days of sick leave annually.
"""


page = ExtractedPage(
    page_number=1,
    text=sample_text,
)

chunks = chunk_pages(
    pages=[page],
    chunk_size=20,
    overlap=5,
)

for chunk in chunks:

    print(f"\nChunk: {chunk.chunk_index}")
    print(f"Page: {chunk.page_number}")
    print(f"Words: {chunk.token_count}")
    print(f"Content:\n{chunk.content}")