from typing import Annotated
from pydantic import BaseModel, Field

# from datetime import datetime


class NoteCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=1, max_length=5000)]
