# AI Manga Translator Pro

Professional starter project for translating manga/manhwa/comic pages inside images.

## Features

- Upload JPG/PNG/WEBP, ZIP, and CBZ chapters.
- Extract and naturally sort pages.
- Backend processing pipeline: OCR -> translation -> text removal -> Arabic rendering.
- Demo mode works without paid AI keys.
- Project API with progress status.
- Web reader for translated chapters.
- Download translated chapter as CBZ.
- Docker Compose for local development.
- GitHub Actions workflow for backend/frontend CI and Docker build.

## Stack

- Backend: Python, FastAPI, Pillow, OpenCV, SQLModel/SQLite
- Frontend: Next.js, React, TypeScript, Tailwind CSS
- CI: GitHub Actions

## Quick start with Docker

```bash
cp .env.example .env
docker compose up --build
```

Frontend: http://localhost:3000  
Backend API: http://localhost:8000/docs

## Local backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Local frontend

```bash
cd frontend
npm install
npm run dev
```

## AI engines

The project ships with a safe demo pipeline:

- OCR: sample detector when no OCR engine is configured.
- Translation: demo Arabic translation placeholder.
- Inpainting: OpenCV/Pillow mask cleaning.
- Arabic rendering: Pillow + arabic-reshaper + python-bidi.

You can replace providers in `backend/app/services/` with PaddleOCR, manga-image-translator, LaMa, OpenAI, DeepL, LibreTranslate, or your own model.

## Legal note

Use this project for content you own, public-domain works, or content you have permission to translate. Do not use it to publish copyrighted chapters without permission.
