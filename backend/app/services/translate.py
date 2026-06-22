import httpx
from app.core.config import settings


class TranslationService:
    async def translate_batch(self, texts: list[str], source: str, target: str) -> list[str]:
        raise NotImplementedError


class DemoTranslator(TranslationService):
    async def translate_batch(self, texts: list[str], source: str, target: str) -> list[str]:
        return ["ترجمة تجريبية: وصّل مزود الترجمة الحقيقي هنا." for _ in texts]


class LibreTranslateService(TranslationService):
    async def translate_batch(self, texts: list[str], source: str, target: str) -> list[str]:
        if not settings.libretranslate_url:
            raise RuntimeError("LIBRETRANSLATE_URL is not configured")
        out: list[str] = []
        async with httpx.AsyncClient(timeout=60) as client:
            for text in texts:
                response = await client.post(
                    f"{settings.libretranslate_url.rstrip('/')}/translate",
                    json={"q": text, "source": source, "target": target, "format": "text"},
                )
                response.raise_for_status()
                out.append(response.json()["translatedText"])
        return out


def get_translator() -> TranslationService:
    if settings.translation_provider == "libretranslate":
        return LibreTranslateService()
    return DemoTranslator()
