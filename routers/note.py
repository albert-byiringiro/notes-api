from fastapi import APIRouter, status, HTTPException
from typing import TypedDict
from schemas.note import NoteCreate, NoteResponse

from datetime import datetime
from zoneinfo import ZoneInfo
import uuid

router = APIRouter(prefix="/notes", tags=["Notes"])


class NoteRecord(TypedDict):
    id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime | None


notes_db: dict[str, NoteRecord] = {}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_note(note: NoteCreate) -> NoteResponse:
    note_id = str(uuid.uuid4())

    record: NoteRecord = {
        "id": note_id,
        "title": note.title,
        "content": note.content,
        "created_at": datetime.now(ZoneInfo("UTC")),
        "updated_at": None,
    }

    notes_db[note_id] = record
    return NoteResponse(**record)


@router.get("/")
async def get_notes() -> list[NoteResponse]:
    return [NoteResponse(**note) for note in notes_db.values()]


@router.get("/{note_id}")
async def get_note(note_id: str) -> NoteResponse:
    if note_id not in notes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Note {note_id} not found"
        )

    return NoteResponse(**notes_db[note_id])


@router.put("/{note_id}")
async def update_note(note_id: str, note: NoteCreate) -> NoteResponse:

    if note_id not in notes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Note {note_id} not found"
        )

    record: NoteRecord = {
        "id": note_id,
        "title": note.title,
        "content": note.content,
        "created_at": notes_db[note_id]["created_at"],
        "updated_at": datetime.now(ZoneInfo("UTC")),
    }

    notes_db[note_id] = record
    return NoteResponse(**record)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str) -> None:
    if note_id not in notes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Note{note_id} not found"
        )

    del notes_db[note_id]
