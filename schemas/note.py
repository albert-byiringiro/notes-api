from pydantic import BaseModel
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    content: str
    created_at: datetime
