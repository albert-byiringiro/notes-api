from fastapi import APIRouter, BackgroundTasks, Depends, status, HTTPException
from typing import Annotated, cast
from dependencies import PaginationParams
from schemas.note import NoteCreate, NoteResponse, NoteUpdate
from services.note import NoteService

from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter(prefix="/notes", tags=["Notes"])


# Dependency factory


def get_note_service() -> NoteService:
    return NoteService()


NotesServiceDep = Annotated[NoteService, Depends(get_note_service)]


def _log_event(event: str, note_id: str, title: str) -> None:
    print(f"[notes] {event}: id={note_id} title={title!r}")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_note(
    note: NoteCreate, service: NotesServiceDep, background_tasks: BackgroundTasks
) -> NoteResponse:
    new_note = service.create(note)
    background_tasks.add_task(_log_event, "created", new_note.id, new_note.title)
    return new_note


@router.get("/")
async def get_notes(
    service: NotesServiceDep,
    pagination: Annotated[PaginationParams, Depends()],
    keyword: str | None = None,
) -> list[NoteResponse]:
    return service.list(skip=pagination.skip, limit=pagination.limit, keyword=keyword)


@router.get("/{note_id}")
async def get_note(note_id: str, service: NotesServiceDep) -> NoteResponse:
    try:
        return service.get(note_id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


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


@router.patch("/{note_id}")
async def patch_note(note_id: str, note: NoteUpdate) -> NoteResponse:
    if note_id not in notes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note {note_id} not found",
        )

    stored = notes_db[note_id]

    updates = note.model_dump(exclude_unset=True)
    if updates:
        stored.update(cast(NoteRecord, updates))
        stored["updated_at"] = datetime.now(ZoneInfo("UTC"))

    return NoteResponse(**stored)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str) -> None:
    if note_id not in notes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Note{note_id} not found"
        )

    del notes_db[note_id]
