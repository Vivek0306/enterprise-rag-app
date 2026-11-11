from app.ingestion.extractor import extract_document


file_path = "data/raw/employee_policy.pdf"

pages = extract_document(file_path)

print("Number of extracted pages:", len(pages))

for page in pages:
    print("\nPage:", page.page_number)
    print("Content:", page.text)