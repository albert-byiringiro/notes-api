from fastapi import APIRouter, status
from typing import List, Optional, TypedDict
from schemas import notes
from datetime import datetime
from zoneinfo import ZoneInfo
import uuid

router = APIRouter(prefix="/notes", tags=["Notes"])


class NoteRecord(TypedDict):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime]


notes_db: List[NoteRecord] = []


@router.get("/", response_model=List[notes.NoteResponse], summary="List all notes")
async def list_notes():
    return notes_db


@router.post(
    "/",
    response_model=notes.NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
)
async def create_note(note_in: notes.NoteCreate):
    now = datetime.now(ZoneInfo("UTC"))
    new_note: NoteRecord = {
        "id": str(uuid.uuid4()),
        "title": note_in.title,
        "content": note_in.content,
        "created_at": now,
        "updated_at": None,
    }
    notes_db.append(new_note)
    return new_note
