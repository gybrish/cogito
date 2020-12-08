from sqlalchemy import Column, Integer, String, DateTime

from file_api.db.database import Base


class FileModel(Base):
    __tablename__ = "files"

    pk = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    id = Column(String, index=True)
    size = Column(Integer)
    created_at = Column(DateTime)
    last_accessed = Column(DateTime)
