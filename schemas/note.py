from typing import Annotated
from pydantic import BaseModel, Field

from datetime import datetime


class NoteBase(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=1, max_length=5000)]


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass


class NoteResponse(NoteBase):
    id: str
    created_at: datetime
    updated_at: datetime | None = None
