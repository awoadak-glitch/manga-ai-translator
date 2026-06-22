import shutil
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from app.core.config import settings
from app.core.database import get_session
from app.models.db import Bubble, Page, Project
from app.services.pipeline import ChapterPipeline
from app.utils.files import ensure_dir, safe_filename

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("")
async def create_project(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form("Untitled Chapter"),
    source_language: str = Form("en"),
    target_language: str = Form("ar"),
    reading_mode: str = Form("webtoon"),
    session: Session = Depends(get_session),
):
    uploads = ensure_dir(Path(settings.media_root) / "_uploads")
    upload_path = uploads / safe_filename(file.filename or "chapter.cbz")
    with open(upload_path, "wb") as out:
        shutil.copyfileobj(file.file, out)

    pipeline = ChapterPipeline(session)
    project = await pipeline.create_project_from_upload(upload_path, title, source_language, target_language, reading_mode)
    background_tasks.add_task(_process, project.id)
    return project


def _process(project_id: str) -> None:
    from sqlmodel import Session
    from app.core.database import engine
    import asyncio

    with Session(engine) as session:
        asyncio.run(ChapterPipeline(session).process_project(project_id))


@router.get("")
def list_projects(session: Session = Depends(get_session)):
    return session.exec(select(Project).order_by(Project.created_at.desc())).all()


@router.get("/{project_id}")
def get_project(project_id: str, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    pages = session.exec(select(Page).where(Page.project_id == project_id).order_by(Page.page_number)).all()
    return {"project": project, "pages": pages}


@router.get("/{project_id}/pages/{page_id}/bubbles")
def page_bubbles(project_id: str, page_id: str, session: Session = Depends(get_session)):
    page = session.get(Page, page_id)
    if not page or page.project_id != project_id:
        raise HTTPException(status_code=404, detail="Page not found")
    return session.exec(select(Bubble).where(Bubble.page_id == page_id)).all()


@router.get("/{project_id}/download.cbz")
def download_cbz(project_id: str, session: Session = Depends(get_session)):
    output = ChapterPipeline(session).export_cbz(project_id)
    return FileResponse(output, media_type="application/vnd.comicbook+zip", filename="chapter_ar.cbz")
