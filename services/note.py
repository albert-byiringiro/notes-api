import uuid
from datetime import datetime
from typing import TypedDict
from zoneinfo import ZoneInfo

from schemas.note import NoteCreate, NoteResponse, NoteUpdate


class NoteRecord(TypedDict):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime | None


class NoteService:
    def __init__(self) -> None:
        self._db: dict[str, NoteRecord] = {}

    def create(self, note: NoteCreate) -> NoteResponse:
        note_id = str(uuid.uuid4())

        record: NoteRecord = {
            "id": note_id,
            "title": note.title,
            "content": note.content,
            "created_at": datetime.now(ZoneInfo("UTC")),
            "updated_at": None,
        }

        self._db[note_id] = record
        return NoteResponse(**record)
