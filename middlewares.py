"""Har bir yangilanishga foydalanuvchi tilini biriktiruvchi middleware."""
from __future__ import annotations

from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import database as db
from i18n import DEFAULT_LANG, LANGS


class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        lang = db.get_lang(user.id) if user else None
        if lang not in LANGS:
            # Telegram mijozi ruscha bo'lsa — ruschani taklif qilamiz
            code = (getattr(user, "language_code", "") or "")[:2]
            lang = "ru" if code == "ru" else DEFAULT_LANG
        data["lang"] = lang
        return await handler(event, data)
