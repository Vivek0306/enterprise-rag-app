
from app.database.connection import SessionLocal
from app.ingestion.service import ingest_document

db = SessionLocal()

try:
    result = ingest_document(
        file_path="data/raw/employee_policy.pdf",
        db=db,
    )

    print("INGESTION RESULT")
    print("----------------")
    for key, value in result.items():
        print(f"{key}: {value}")

finally:
    db.close()
