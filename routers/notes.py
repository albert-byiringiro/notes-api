from datetime import datetime
from fastapi import APIRouter
from typing import List, Optional, TypedDict

router = APIRouter(prefix="/notes", tags=["Notes"])


class NoteRecord(TypedDict):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime]


notes_db: List[NoteRecord] = []
