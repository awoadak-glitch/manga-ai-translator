# Architecture

## Pipeline

1. Upload: file is saved in `MEDIA_ROOT/_uploads`.
2. Extract: ZIP/CBZ is extracted into `project/original`.
3. OCR: `OCRService.detect()` returns text regions.
4. Translate: `TranslationService.translate_batch()` translates regions with page context.
5. Inpaint: `InpaintService.clean_text_regions()` removes source text.
6. Render: `ArabicRenderer.draw_translations()` writes Arabic RTL text.
7. Reader: frontend reads translated image URLs from the backend.
8. Export: backend packs translated pages into CBZ.

## Replace demo AI with production providers

- OCR: replace `DemoOCR` in `services/ocr.py` with PaddleOCR/EasyOCR/custom model.
- Translator: add provider in `services/translate.py`.
- Inpainting: replace OpenCV Telea with LaMa or manga-specific inpainting.
- Balloon detection: add YOLO/segmentation model and merge its boxes with OCR boxes.

## Production recommendations

- Use PostgreSQL instead of SQLite.
- Use S3-compatible object storage instead of local disk.
- Move processing to Celery/RQ workers.
- Add auth and per-user storage quotas.
- Add manual editor for bubble correction.
