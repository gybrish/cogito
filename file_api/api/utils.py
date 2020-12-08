from fastapi import Response
from fastapi.responses import StreamingResponse
from hashlib import sha256
from io import BytesIO
from typing import List
import zipfile

from file_api.db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_path(filename: str) -> str:
    return f"uploads/{filename}"


def get_id(filename: str) -> str:
    return sha256(filename.encode("utf-8")).hexdigest()


def zip_file_in_memory(filename: str) -> Response:
    return zip_files_in_memory([filename])


def zip_files_in_memory(filenames: List[str]) -> Response:
    zipped_file = BytesIO()
    with zipfile.ZipFile(zipped_file, "w", zipfile.ZIP_DEFLATED) as zipped:
        for filename in filenames:
            zipped.write(get_path(filename), filename)

    zipped_file.seek(0)
    response = StreamingResponse(zipped_file, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = "attachment; filename=test.zip"
    return response
