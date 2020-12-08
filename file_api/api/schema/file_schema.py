from pydantic import BaseModel
from datetime import datetime


class FileSchema(BaseModel):
    name: str
    size: int
    created_at: datetime
    id: str

    class Config:
        orm_mode = True
