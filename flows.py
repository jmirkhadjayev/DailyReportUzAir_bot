"""Bir nechta handlerda ishlatiladigan umumiy oqimlar."""
from __future__ import annotations

from datetime import date

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import database as db
import keyboards as kb
from i18n import t
from states import ReportForm
from utils import esc, fmt_date, iso, shorten

MAX_PAST_DAYS = 30
FIELD_LIMIT = 3000


async def ask_done(message: Message, state: FSMContext, lang: str, mode: str) -> None:
    """«Bajarilgan ishlar» savolini beradi."""
    await state.set_state(ReportForm.done)
    await state.update_data(mode=mode)
    note = t(lang, "append_note") if mode == "add" else ""
    await message.answer(t(lang, "ask_done") + note, reply_markup=kb.cancel_kb(lang))


async def begin_report(message: Message, state: FSMContext, lang: str, employee, day: date) -> None:
    """Tanlangan kun uchun hisobotni boshlaydi.

    Agar o'sha kunga hisobot bo'lsa — qo'shishmi yoki almashtirishmi deb so'raydi
    (hodim kun davomida bir necha marta yozishi mumkin).
    """
    await state.update_data(report_date=iso(day), employee_id=employee["id"])

    existing = db.get_report(employee["id"], iso(day))
    if existing is None:
        await ask_done(message, state, lang, "new")
        return

    await state.set_state(ReportForm.choosing_mode)
    await message.answer(
        t(
            lang,
            "report_exists_choice",
            date=fmt_date(day),
            preview=esc(shorten(existing["done"], 400)),
        ),
        reply_markup=kb.report_mode_kb(lang),
    )
