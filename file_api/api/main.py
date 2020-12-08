from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from file_api.db.database import Base, engine
from file_api.db import db_helpers
from file_api.api.schema.file_schema import FileSchema
from file_api.api.utils import (
    get_db,
    get_path,
    get_id,
    zip_file_in_memory,
    zip_files_in_memory,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/store", response_model=FileSchema)
async def create_upload_file(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    # Assuming memory alwyas has space for uploaded file before write
    content = await file.read()
    path = get_path(file.filename)
    with open(path, "wb+") as fout:
        fout.write(content)

    file_details = FileSchema(
        name=file.filename,
        size=len(content),
        created_at=datetime.utcnow(),
        id=get_id(file.filename),
    )
    return db_helpers.add_file(db, file_details)


@app.get("/files", response_model=List[FileSchema])
async def get_files(db: Session = Depends(get_db)):
    return db_helpers.get_files(db)


@app.get("/files/{id}", response_model=FileSchema)
async def get_file(id: str, db: Session = Depends(get_db)):
    file = db_helpers.get_file_by_id(db, id)
    if file is None:
        raise HTTPException(status_code=404, detail=f"file {id} not found")

    return file


@app.get("/files/{id}/zip")
def get_zipped_file(id: str, db: Session = Depends(get_db)):
    db_file = db_helpers.get_file_by_id(db, id)
    return zip_file_in_memory(db_file.name)


@app.get("/mrufiles", response_model=List[FileSchema])
async def get_mru_files(n: int, db: Session = Depends(get_db)):
    return db_helpers.get_recently_used(db, n)


@app.get("/mrufiles/zip")
def get_mru_files_zipped(n: int, db: Session = Depends(get_db)):
    file_list = db_helpers.get_recently_used(db, n)
    if not file_list:
        raise HTTPException(status_code=404, detail="No recently used files")

    file_names = [file.name for file in file_list]
    return zip_files_in_memory(file_names)
