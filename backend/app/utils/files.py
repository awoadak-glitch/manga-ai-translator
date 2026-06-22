import os
import shutil
import zipfile
from pathlib import Path
from natsort import natsorted

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ARCHIVE_EXTENSIONS = {".zip", ".cbz"}


def safe_filename(name: str) -> str:
    return "".join(ch for ch in name if ch.isalnum() or ch in "._- ").strip() or "chapter"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def extract_input(upload_path: Path, target_dir: Path) -> list[Path]:
    ensure_dir(target_dir)
    suffix = upload_path.suffix.lower()
    if suffix in ARCHIVE_EXTENSIONS:
        with zipfile.ZipFile(upload_path) as zf:
            for member in zf.infolist():
                if member.is_dir():
                    continue
                name = Path(member.filename).name
                if Path(name).suffix.lower() in IMAGE_EXTENSIONS:
                    out = target_dir / safe_filename(name)
                    with zf.open(member) as src, open(out, "wb") as dst:
                        shutil.copyfileobj(src, dst)
    elif suffix in IMAGE_EXTENSIONS:
        shutil.copy2(upload_path, target_dir / upload_path.name)
    else:
        raise ValueError("Unsupported file type. Use images, ZIP, or CBZ.")

    images = [p for p in target_dir.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS]
    return list(natsorted(images, key=lambda p: p.name))


def make_cbz(image_paths: list[Path], output_path: Path) -> Path:
    ensure_dir(output_path.parent)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for idx, image_path in enumerate(image_paths, start=1):
            arcname = f"{idx:03d}{image_path.suffix.lower()}"
            zf.write(image_path, arcname=arcname)
    return output_path
