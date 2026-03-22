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

    def list(
        self,
        skip: int = 0,
        limit: int = 10,
        keyword: str | None = None,
    ) -> list[NoteResponse]:
        notes = list(self._db.values())
        if keyword is not None:
            search = keyword.lower()
            notes = [
                n
                for n in notes
                if search in n["title"].lower() or search in n["content"].lower()
            ]
        return [NoteResponse(**n) for n in notes[skip : skip + limit]]

    def get(self, note_id: str) -> NoteResponse:
        if note_id not in self._db:
            raise KeyError(f"Note {note_id} not found")

        return NoteResponse(**self._db[note_id])

    def update(self, note_id: str, note: NoteCreate) -> NoteResponse:
        if note_id not in self._db:
            raise KeyError(f"Note {note_id} not found")

        record: NoteRecord = {
            "id": note_id,
            "title": note.title,
            "content": note.content,
            "created_at": self._db[note_id]["created_at"],
            "updated_at": datetime.now(ZoneInfo("UTC")),
        }

        self._db[note_id] = record
        return NoteResponse(**record)
