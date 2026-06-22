from pathlib import Path
from textwrap import wrap
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from .ocr import TextRegion


class ArabicRenderer:
    def __init__(self) -> None:
        self.font_candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]

    def _font(self, size: int) -> ImageFont.FreeTypeFont:
        for path in self.font_candidates:
            if Path(path).exists():
                return ImageFont.truetype(path, size=size)
        return ImageFont.load_default()

    def _rtl(self, text: str) -> str:
        return get_display(arabic_reshaper.reshape(text))

    def draw_translations(self, cleaned_path: Path, regions: list[TextRegion], translations: list[str], output_path: Path) -> Path:
        image = Image.open(cleaned_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        for region, text in zip(regions, translations):
            size = max(16, min(34, int(region.h / 3)))
            font = self._font(size)
            max_chars = max(8, int(region.w / max(size * 0.55, 1)))
            lines = wrap(text, width=max_chars)
            shaped_lines = [self._rtl(line) for line in lines]
            line_height = int(size * 1.35)
            total_h = line_height * len(shaped_lines)
            y = region.y + max(0, (region.h - total_h) // 2)
            for line in shaped_lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_w = bbox[2] - bbox[0]
                x = region.x + max(0, (region.w - text_w) // 2)
                draw.text((x, y), line, fill=(0, 0, 0), font=font)
                y += line_height
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, quality=95)
        return output_path
