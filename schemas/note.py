# schemas/note.py
from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):

    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=1, max_length=5000)]


class NoteCreate(NoteBase):

    pass


class NoteUpdate(BaseModel):
    title: Annotated[Optional[str], Field(default=None, min_length=1, max_length=200)]
    content: Annotated[
        Optional[str], Field(default=None, min_length=1, max_length=5000)
    ]


class NoteResponse(NoteBase):

    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
