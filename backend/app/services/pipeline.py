import uuid
from pathlib import Path
from sqlmodel import Session, select
from app.core.config import settings
from .ocr import DemoOCR
from app.models.db import Bubble, Page, Project, ProjectStatus
from app.utils.files import ensure_dir, extract_input, make_cbz
from .translate import get_translator
from .inpaint import InpaintService
from .render import ArabicRenderer


class ChapterPipeline:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.media_root = Path(settings.media_root)
        self.ocr = DemoOCR()
        self.translator = get_translator()
        self.inpaint = InpaintService()
        self.renderer = ArabicRenderer()

    async def create_project_from_upload(
        self,
        upload_path: Path,
        title: str,
        source_language: str,
        target_language: str,
        reading_mode: str,
    ) -> Project:
        project = Project(
            id=str(uuid.uuid4()),
            title=title,
            source_language=source_language,
            target_language=target_language,
            reading_mode=reading_mode,
        )
        self.session.add(project)
        self.session.commit()

        project_dir = self.media_root / project.id
        originals = ensure_dir(project_dir / "original")
        images = extract_input(upload_path, originals)
        for idx, image in enumerate(images, start=1):
            self.session.add(Page(
                id=str(uuid.uuid4()),
                project_id=project.id,
                page_number=idx,
                original_path=str(image),
            ))
        self.session.commit()
        return project

    async def process_project(self, project_id: str) -> None:
        project = self.session.get(Project, project_id)
        if not project:
            return
        try:
            project.status = ProjectStatus.processing
            project.progress = 1
            self.session.add(project)
            self.session.commit()

            pages = self.session.exec(select(Page).where(Page.project_id == project_id).order_by(Page.page_number)).all()
            total = max(1, len(pages))
            output_dir = ensure_dir(self.media_root / project_id / "translated")
            clean_dir = ensure_dir(self.media_root / project_id / "cleaned")

            for index, page in enumerate(pages, start=1):
                page.status = ProjectStatus.processing
                self.session.add(page)
                self.session.commit()

                original = Path(page.original_path)
                regions = self.ocr.detect(original)
                texts = [r.text for r in regions]
                translations = await self.translator.translate_batch(texts, project.source_language, project.target_language)

                clean_path = clean_dir / f"{page.page_number:03d}.jpg"
                translated_path = output_dir / f"{page.page_number:03d}.jpg"
                self.inpaint.clean_text_regions(original, regions, clean_path)
                self.renderer.draw_translations(clean_path, regions, translations, translated_path)

                page.translated_path = str(translated_path)
                page.status = ProjectStatus.completed
                self.session.add(page)

                for region, text, translation in zip(regions, texts, translations):
                    self.session.add(Bubble(
                        id=str(uuid.uuid4()),
                        page_id=page.id,
                        x=region.x,
                        y=region.y,
                        w=region.w,
                        h=region.h,
                        original_text=text,
                        translated_text=translation,
                    ))

                project.progress = int(index / total * 100)
                self.session.add(project)
                self.session.commit()

            project.status = ProjectStatus.completed
            project.progress = 100
            self.session.add(project)
            self.session.commit()
        except Exception as exc:  # noqa: BLE001
            project.status = ProjectStatus.failed
            project.error = str(exc)
            self.session.add(project)
            self.session.commit()

    def export_cbz(self, project_id: str) -> Path:
        pages = self.session.exec(select(Page).where(Page.project_id == project_id).order_by(Page.page_number)).all()
        translated = [Path(p.translated_path) for p in pages if p.translated_path]
        if not translated:
            raise RuntimeError("Project has no translated pages yet")
        return make_cbz(translated, self.media_root / project_id / "exports" / "chapter_ar.cbz")
