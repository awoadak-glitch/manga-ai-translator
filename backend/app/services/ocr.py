from dataclasses import dataclass
from pathlib import Path
from PIL import Image


@dataclass
class TextRegion:
    x: int
    y: int
    w: int
    h: int
    text: str


class OCRService:
    """Provider interface. Replace DemoOCR with PaddleOCR/EasyOCR for production."""

    def detect(self, image_path: Path) -> list[TextRegion]:
        raise NotImplementedError


class DemoOCR(OCRService):
    def detect(self, image_path: Path) -> list[TextRegion]:
        image = Image.open(image_path)
        w, h = image.size
        # Demo region so the full app works immediately.
        return [
            TextRegion(
                x=max(20, w // 12),
                y=max(20, h // 12),
                w=max(180, w // 3),
                h=max(90, h // 10),
                text="Demo text: configure PaddleOCR to read real bubbles.",
            )
        ]
