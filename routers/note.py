from fastapi import APIRouter, status, HTTPException, Query
from typing import List, Optional, TypedDict, cast, Annotated
from schemas.note import NoteCreate, NoteResponse, NoteUpdate

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
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
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


@router.get(
    "/",
    response_model=List[note.NoteResponse],
    summary="List all notes (with optional pagination & title filter)",
)
async def list_notes(
    skip: Annotated[
        int, Query(ge=0, description="Number of records to skip (offset)")
    ] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Max number of records to return")
    ] = 10,
    title: Annotated[
        Optional[str],
        Query(description="Filter by title (case-insensitive partial match)"),
    ] = None,
):
    filtered_notes = notes_db

    if title:
        title_lower = title.lower()
        filtered_notes = [
            note for note in filtered_notes if title_lower in note["title"].lower()
        ]

    paginated_notes = filtered_notes[skip : skip + limit]

    return paginated_notes


@router.get("/{note_id}", response_model=note.NoteResponse, summary="Get a note by ID")
async def get_note(note_id: str):
    note = find_note(note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.patch(
    "/{note_id}", response_model=note.NoteResponse, summary="Partial update a note"
)
async def update_note(note_id: str, note_update: note.NoteUpdate):
    note = find_note(note_id)
    now = datetime.now(ZoneInfo("UTC"))

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    update_data = note_update.model_dump(exclude_unset=True)
    if update_data:
        note.update(cast(NoteRecord, update_data))
        note["updated_at"] = now

    return note


@router.put(
    "/{note}", response_model=note.NoteResponse, summary="Full update (replace) a note"
)
async def replace_note(note_id: str, note_in: note.NoteCreate):
    note = find_note(note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    now = datetime.now(ZoneInfo("UTC"))

    note["title"] = note_in.title
    note["content"] = note_in.content
    note["updated_at"] = now

    return note


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a note")
async def delele_note(note_id: str):
    note = find_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    notes_db.remove(note)
    return None
