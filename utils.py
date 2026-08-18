"""Sana va matn bilan ishlash uchun yordamchi funksiyalar."""
from __future__ import annotations

import html
import re
from datetime import date, datetime, timedelta

from config import TZ

WEEKDAYS = {
    "uz": ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"],
    "ru": ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"],
}
MONTHS = {
    "uz": ["yanvar", "fevral", "mart", "aprel", "may", "iyun",
           "iyul", "avgust", "sentyabr", "oktyabr", "noyabr", "dekabr"],
    "ru": ["января", "февраля", "марта", "апреля", "мая", "июня",
           "июля", "августа", "сентября", "октября", "ноября", "декабря"],
}


def today() -> date:
    return datetime.now(TZ).date()


def now_str() -> str:
    return datetime.now(TZ).strftime("%d.%m.%Y %H:%M")


def now_time() -> str:
    return datetime.now(TZ).strftime("%H:%M")


def iso(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def fmt_date(value: str | date) -> str:
    """2026-08-18 -> 18.08.2026"""
    d = parse_iso(value) if isinstance(value, str) else value
    return d.strftime("%d.%m.%Y") if d else str(value)


def fmt_date_long(value: str | date, lang: str = "uz") -> str:
    """uz: 18-avgust, 2026-yil (Seshanba)   |   ru: 18 августа 2026 г. (вторник)"""
    d = parse_iso(value) if isinstance(value, str) else value
    if not d:
        return str(value)
    months = MONTHS.get(lang, MONTHS["uz"])
    weekdays = WEEKDAYS.get(lang, WEEKDAYS["uz"])
    if lang == "ru":
        return f"{d.day} {months[d.month - 1]} {d.year} г. ({weekdays[d.weekday()]})"
    return f"{d.day}-{months[d.month - 1]}, {d.year}-yil ({weekdays[d.weekday()]})"


def parse_iso(value: str) -> date | None:
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


def parse_user_date(value: str) -> date | None:
    """Foydalanuvchi kiritgan sanani tushunadi: 18.08.2026, 18/08/2026, 2026-08-18."""
    value = value.strip()
    for fmt in ("%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d.%m.%y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def parse_period_input(text: str) -> tuple[date, date] | None:
    """"18.08.2026" yoki "01.08.2026 - 18.08.2026" ko'rinishidagi davrni o'qiydi."""
    tokens = re.findall(r"\d{1,4}[./-]\d{1,2}[./-]\d{2,4}", text)
    dates = [d for d in (parse_user_date(tok) for tok in tokens) if d]
    if not dates:
        return None
    if len(dates) == 1:
        return dates[0], dates[0]
    start, end = dates[0], dates[1]
    return (start, end) if start <= end else (end, start)


def resolve_period(code: str) -> tuple[date, date]:
    t = today()
    if code == "today":
        return t, t
    if code == "yesterday":
        y = t - timedelta(days=1)
        return y, y
    if code == "week":
        return t - timedelta(days=t.weekday()), t
    if code == "last7":
        return t - timedelta(days=6), t
    if code == "month":
        return t.replace(day=1), t
    if code == "last30":
        return t - timedelta(days=29), t
    return t, t


def period_title(date_from: date, date_to: date, lang: str = "uz") -> str:
    if date_from == date_to:
        return fmt_date_long(date_from, lang)
    return f"{fmt_date(date_from)} — {fmt_date(date_to)}"


def esc(text: str | None) -> str:
    return html.escape(text or "")


def shorten(text: str, limit: int = 300) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def safe_filename(text: str) -> str:
    return re.sub(r"[^0-9A-Za-z_.-]+", "_", text).strip("_") or "hisobot"
