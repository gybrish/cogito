from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional

from file_api.model.file_model import FileModel
from file_api.api.schema.file_schema import FileSchema


def get_file_by_id(db: Session, file_id: str) -> Optional[FileModel]:
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if db_file is None:
        return None

    db_file.last_accessed = datetime.utcnow()
    db.commit()
    return db_file


def get_files(db: Session) -> Optional[List[FileModel]]:
    return db.query(FileModel).order_by(FileModel.name).all()


def _get_default_date() -> datetime:
    return datetime.fromisoformat("2020-01-01T12:00:00+00:00")


def add_file(db: Session, file: FileSchema) -> FileModel:
    # defaulting last accessed to time before app was deployed
    db_file = FileModel(**file.dict(), last_accessed=_get_default_date())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_recently_used(db: Session, limit: int) -> Optional[List[FileModel]]:
    return (
        db.query(FileModel).order_by(FileModel.last_accessed.desc()).limit(limit).all()
    )
