"""Maxsus filtrlar."""
from __future__ import annotations

from aiogram.filters import BaseFilter
from aiogram.types import Message, TelegramObject

import i18n
from config import is_admin


class Btn(BaseFilter):
    """Tugma matni — barcha tillardagi variantlari bilan solishtiriladi."""

    def __init__(self, *keys: str) -> None:
        self.values: set[str] = set()
        for key in keys:
            self.values |= i18n.all_variants(key)

    async def __call__(self, message: Message) -> bool:
        return bool(message.text) and message.text in self.values


class IsAdmin(BaseFilter):
    async def __call__(self, event: TelegramObject) -> bool:
        user = getattr(event, "from_user", None)
        return bool(user and is_admin(user.id))
