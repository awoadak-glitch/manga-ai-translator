from datetime import datetime, timezone
from enum import Enum
from sqlmodel import Field, SQLModel


class ProjectStatus(str, Enum):
    uploaded = "uploaded"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Project(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str
    source_language: str = "en"
    target_language: str = "ar"
    reading_mode: str = "webtoon"
    status: ProjectStatus = ProjectStatus.uploaded
    progress: int = 0
    error: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Page(SQLModel, table=True):
    id: str = Field(primary_key=True)
    project_id: str = Field(index=True)
    page_number: int
    original_path: str
    translated_path: str | None = None
    status: ProjectStatus = ProjectStatus.uploaded


class Bubble(SQLModel, table=True):
    id: str = Field(primary_key=True)
    page_id: str = Field(index=True)
    x: int
    y: int
    w: int
    h: int
    original_text: str
    translated_text: str
    font_size: int = 28
