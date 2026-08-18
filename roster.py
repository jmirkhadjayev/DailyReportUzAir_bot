"""Shtat ro'yxati: tabel raqami — F.I.Sh. — lavozim.

Ma'lumot `staff.json` faylidan o'qiladi (u GitHubga tushmaydi — .gitignore da).
Fayl yo'li `STAFF_FILE` muhit o'zgaruvchisi orqali almashtiriladi, masalan
Render'da: STAFF_FILE=/etc/secrets/staff.json

Yangi hodim qo'shish / lavozimni o'zgartirish: staff.json ni tahrirlab,
botni qayta ishga tushiring. Fayl namunasi — staff.example.json.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

from config import BASE_DIR, STAFF_FILE

log = logging.getLogger(__name__)

EXAMPLE_FILE = BASE_DIR / "staff.example.json"
PAGE_SIZE = 8


def load_staff(path: Path | None = None) -> list[dict[str, str]]:
    """Shtat ro'yxatini fayldan o'qiydi."""
    source = path or STAFF_FILE
    if not source.exists():
        if EXAMPLE_FILE.exists():
            log.warning(
                "%s topilmadi — namuna ro'yxat (%s) ishlatilmoqda. "
                "Haqiqiy ro'yxatni staff.json ga yozing.",
                source.name,
                EXAMPLE_FILE.name,
            )
            source = EXAMPLE_FILE
        else:
            log.error("Shtat ro'yxati topilmadi: %s — hech kim ro'yxatdan o'ta olmaydi.", source)
            return []

    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        log.error("Shtat ro'yxatini o'qib bo'lmadi (%s): %s", source, exc)
        return []

    staff: list[dict[str, str]] = []
    for item in data:
        tabel = str(item.get("tabel", "")).strip()
        full_name = str(item.get("full_name", "")).strip()
        if not tabel or not full_name:
            log.warning("Shtat ro'yxatidagi to'liqsiz yozuv o'tkazib yuborildi: %s", item)
            continue
        staff.append(
            {"tabel": tabel, "full_name": full_name, "position": str(item.get("position", "")).strip()}
        )
    log.info("Shtat ro'yxati yuklandi: %s ta hodim (%s)", len(staff), source.name)
    return staff


STAFF: list[dict[str, str]] = load_staff()


def by_index(index: int) -> dict[str, str] | None:
    return STAFF[index] if 0 <= index < len(STAFF) else None


def by_tabel(tabel: str) -> dict[str, str] | None:
    """Tabel raqami bo'yicha qidiradi ('12' ham '0012' ni topadi)."""
    tabel = (tabel or "").strip()
    if not tabel:
        return None
    for person in STAFF:
        if person["tabel"] == tabel:
            return person
    if tabel.isdigit():
        for person in STAFF:
            if person["tabel"].isdigit() and int(person["tabel"]) == int(tabel):
                return person
    return None


def find_by_name(full_name: str) -> dict[str, str] | None:
    """To'liq yozilgan F.I.Sh. bo'yicha shtat ro'yxatidan qidiradi."""
    normalized = _norm(full_name)
    for person in STAFF:
        if _norm(person["full_name"]) == normalized:
            return person
    return None


def position_of(full_name: str) -> str:
    """F.I.Sh. bo'yicha lavozim (topilmasa — bo'sh satr)."""
    person = find_by_name(full_name)
    return person["position"] if person else ""


def search(query: str) -> list[tuple[int, dict[str, str]]]:
    """F.I.Sh. yoki tabel raqami bo'yicha qidiradi."""
    q = _norm(query)
    if not q:
        return []
    return [
        (i, person)
        for i, person in enumerate(STAFF)
        if q in _norm(person["full_name"]) or q in person["tabel"]
    ]


def page_count() -> int:
    return (len(STAFF) + PAGE_SIZE - 1) // PAGE_SIZE


def page_items(page: int) -> list[tuple[int, dict[str, str]]]:
    start = page * PAGE_SIZE
    return list(enumerate(STAFF))[start : start + PAGE_SIZE]


def _norm(text: str) -> str:
    """Qidiruv uchun: kichik harf, apostrof va ortiqcha bo'shliqlarsiz."""
    text = (text or "").lower().strip()
    for ch in "'’`‘ʻ":
        text = text.replace(ch, "")
    return " ".join(text.split())
