# Simple Notes REST API

A lightweight, in-memory REST API for managing notes, built with **FastAPI**.

Created as a mini-project to demonstrate:
- Modern FastAPI structure and best practices
- Pydantic for validation & serialization
- In-memory storage (no database — easy to swap later)
- CRUD operations with proper HTTP semantics
- Partial & full updates (PATCH + PUT)
- Pagination & basic filtering
- Type-safe code with modern Python typing

## Features

- **Create** a note (POST)
- **Read** all notes or single note (GET)
- **Update** partially (PATCH) or fully (PUT)
- **Delete** a note (DELETE)
- Pagination (`?skip=` & `?limit=`)
- Case-insensitive title filtering (`?title=`)
- Server-controlled timestamps (created_at / updated_at)
- Automatic OpenAPI docs (Swagger UI / ReDoc)
- Clean separation: router, schemas, in-memory "DB"

## Tech Stack

- **FastAPI** — modern, fast, async-first web framework
- **Pydantic v2** — data validation, serialization, OpenAPI generation
- **Uvicorn** — ASGI server
- Python 3.10+ features: union types (`str | None`), `Annotated`, etc.
- No external dependencies beyond FastAPI & its requirements

## Project Structure

```
project/
├── main.py               # App entry point (imports router)
├── api/
│   └── routers/
│       └── notes.py      # All endpoints + in-memory storage
├── schemas/
│   └── notes.py          # Pydantic models: NoteCreate, NoteUpdate, NoteResponse
└── README.md
```

## Endpoints Overview

| Method | Endpoint              | Description                              | Query Params              |
|--------|-----------------------|------------------------------------------|---------------------------|
| POST   | `/notes/`             | Create a new note                        | —                         |
| GET    | `/notes/`             | List notes (paginated & filtered)        | `skip`, `limit`, `title`  |
| GET    | `/notes/{note_id}`    | Get single note by ID                    | —                         |
| PATCH  | `/notes/{note_id}`    | Partial update (only sent fields)        | —                         |
| PUT    | `/notes/{note_id}`    | Full replacement update                  | —                         |
| DELETE | `/notes/{note_id}`    | Delete a note                            | —                         |

**Response model** for all read/create/update operations:
```json
{
  "id": "uuid-string",
  "title": "string",
  "content": "string",
  "created_at": "2026-03-18T14:30:00+00:00",
  "updated_at": "2026-03-18T15:45:00+00:00" | null
}
```

## How to Run

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   # or with poetry/pipenv/uv/...
   ```

2. Run the server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

3. Open interactive docs:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc:     http://127.0.0.1:8000/redoc

## Example Requests (curl)

```bash
# Create note
curl -X POST "http://127.0.0.1:8000/notes/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Meeting Notes", "content": "Discuss Q2 roadmap"}'

# List with filter & pagination
curl "http://127.0.0.1:8000/notes/?title=meeting&limit=5"

# Partial update
curl -X PATCH "http://127.0.0.1:8000/notes/<uuid>" \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated: Include budget discussion"}'

# Full replace
curl -X PUT "http://127.0.0.1:8000/notes/<uuid>" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title", "content": "Completely new content"}'
```

## Next Steps / Improvements (possible future versions)

- Add SQLite / PostgreSQL persistence (SQLModel or SQLAlchemy)
- Add sorting (`?sort=created_at:desc`)
- Add response metadata (total count, has_more)
- Basic authentication (API key or JWT)
- Input sanitization / XSS prevention (if rendering content)
- Unit tests with pytest + TestClient
- Docker support

## Notes

- Data is **in-memory only** — restarting the server clears everything.
- Timestamps are **UTC** and set server-side for consistency & security.
- Designed to be easy to evolve into a production-grade API.