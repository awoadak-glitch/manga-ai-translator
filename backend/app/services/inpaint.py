from pathlib import Path
import cv2
import numpy as np
from PIL import Image
from .ocr import TextRegion


class InpaintService:
    def clean_text_regions(self, image_path: Path, regions: list[TextRegion], output_path: Path) -> Path:
        image = cv2.imread(str(image_path))
        if image is None:
            raise RuntimeError(f"Could not read image: {image_path}")
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        for region in regions:
            pad = 8
            x1 = max(0, region.x - pad)
            y1 = max(0, region.y - pad)
            x2 = min(image.shape[1], region.x + region.w + pad)
            y2 = min(image.shape[0], region.y + region.h + pad)
            mask[y1:y2, x1:x2] = 255
        cleaned = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_path), cleaned)
        return output_path
