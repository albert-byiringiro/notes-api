from fastapi import APIRouter, status, HTTPException, Query
from typing import List, Optional, TypedDict, cast, Annotated
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


def find_note(note_id: str) -> NoteRecord | None:
    for note in notes_db:
        if note["id"] == note_id:
            return note

    return None


@router.get(
    "/",
    response_model=List[notes.NoteResponse],
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


@router.get("/{note_id}", response_model=notes.NoteResponse, summary="Get a note by ID")
async def get_note(note_id: str):
    note = find_note(note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.patch(
    "/{note_id}", response_model=notes.NoteResponse, summary="Partial update a note"
)
async def update_note(note_id: str, note_update: notes.NoteUpdate):
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
    "/{note}", response_model=notes.NoteResponse, summary="Full update (replace) a note"
)
async def replace_note(note_id: str, note_in: notes.NoteCreate):
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
