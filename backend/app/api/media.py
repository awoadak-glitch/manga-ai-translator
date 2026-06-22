from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.core.config import settings

router = APIRouter(prefix="/media", tags=["media"])


@router.get("/{project_id}/{folder}/{filename}")
def get_media(project_id: str, folder: str, filename: str):
    allowed = {"original", "translated", "cleaned"}
    if folder not in allowed:
        raise HTTPException(status_code=400, detail="Invalid folder")
    path = Path(settings.media_root) / project_id / folder / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Media not found")
    return FileResponse(path)
