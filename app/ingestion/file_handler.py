from datetime import datetime, timezone
from pathlib import Path
import  hashlib

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


def validate_file(file_path: str) -> Path:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File does not exist: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Expected a file, received: {path}"
        )

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format: {path.suffix}"
        )

    return path


def calculate_checksum(file_path: Path) -> str:
    sha256_hash = hashlib.sha256()

    with file_path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            sha256_hash.update(block)

    return sha256_hash.hexdigest()

def extract_file_metadata(file_path: Path) -> dict:

    stat = file_path.stat()

    metadata = {
        "filename": file_path.name,
        "file_path": str(file_path.resolve()),
        "file_extension": file_path.suffix.lower(),
        "file_size_bytes": file_path.stat().st_size,
        "checksum": calculate_checksum(file_path),
        "last_modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
    }
    return metadata