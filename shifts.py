"""Smenalar va ish grafiklarini hisoblash moduli.

- 7 ta xodim: 4 ta smenada (KUN: 08:00-20:00, TUN: 20:00-08:00)
  Rotatsiya 4 kunlik sikl asosida (boshlanish sanasi: 21.08.2026).
- Qolgan barcha xodimlar: 5 kunlik standart ish rejimi (Du-Ju 09:00-18:00).
"""
from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Optional

# 4 ta smena tarkibi (tabel raqamlari)
SHIFTS: dict[int, list[str]] = {
    1: ["6598", "1202"],
    2: ["0003", "6688"],
    3: ["6613", "7040"],
    4: ["5699"],
}

# Barcha smenali xodimlarning tabel raqamlari
SHIFT_WORKER_TABELS: set[str] = {tabel for tabels in SHIFTS.values() for tabel in tabels}

# Rotatsiya boshlang'ich nuqtasi (Anchor)
ANCHOR_DATE = date(2026, 8, 21)

# Kunduzgi (08:00 - 20:00) va Tungi (20:00 - 08:00) navbatlar sikli
DAY_ROTATION = [2, 1, 3, 4]    # 21.08: 2-smena, 22.08: 1-smena, 23.08: 3-smena, 24.08: 4-smena
NIGHT_ROTATION = [2, 4, 1, 3]  # 21.08: 2-smena, 22.08: 4-smena, 23.08: 1-smena, 24.08: 3-smena


def is_shift_worker(tabel: str) -> bool:
    """Xodim smenali ish rejimida ekanligini tekshiradi."""
    tabel_clean = (tabel or "").strip()
    return tabel_clean in SHIFT_WORKER_TABELS or (
        tabel_clean.isdigit() and any(int(t) == int(tabel_clean) for t in SHIFT_WORKER_TABELS)
    )


def get_employee_shift_num(tabel: str) -> Optional[int]:
    """Xodim qaysi smenaga tegishli ekanligini aniqlaydi (1, 2, 3, 4 yoki None)."""
    tabel_clean = (tabel or "").strip()
    for shift_num, tabels in SHIFTS.items():
        if tabel_clean in tabels:
            return shift_num
        if tabel_clean.isdigit() and any(int(t) == int(tabel_clean) for t in tabels):
            return shift_num
    return None


def get_shifts_for_date(target_date: date) -> tuple[int, int]:
    """Berilgan sana uchun (KUN smenasi raqami, TUN smenasi raqami) qaytaradi."""
    delta_days = (target_date - ANCHOR_DATE).days
    idx = delta_days % 4
    return DAY_ROTATION[idx], NIGHT_ROTATION[idx]


def is_on_duty(tabel: str, target_date: date, check_time: time | None = None) -> bool:
    """Xodim ko'rsatilgan sana va vaqtda navbatchi (ishda) ekanligini aniqlaydi.
    
    - 5 kunlik xodimlar: Du-Ju ishlaydi (agar check_time berilsa: 08:00 - 19:00 oralig'i).
    - Smenali xodimlar: o'zining KUN (08:00-20:00) yoki TUN (20:00-08:00) smenasida ishlaydi.
    """
    shift_num = get_employee_shift_num(tabel)

    # 1. Standart 5 kunlik xodimlar
    if shift_num is None:
        if target_date.weekday() >= 5:  # Shanba (5) yoki Yakshanba (6)
            return False
        if check_time is not None:
            # 08:00 dan 19:00 gacha faol hisoblanadi
            return time(8, 0) <= check_time <= time(19, 0)
        return True

    # 2. Smenali xodimlar
    day_shift, night_shift = get_shifts_for_date(target_date)

    if check_time is None:
        # Sana bo'yicha umumiy tekshiruv (shu kuni KUN yoki TUN smenasi bormi)
        return (shift_num == day_shift) or (shift_num == night_shift)

    # Aniq vaqt bo'yicha tekshiruv
    if time(8, 0) <= check_time < time(20, 0):
        # Kunduzgi smena vaqti (08:00 - 20:00)
        return shift_num == day_shift
    elif check_time >= time(20, 0):
        # Bugungi tungi smena boshlanishi (20:00 - 23:59)
        return shift_num == night_shift
    else:
        # 00:00 dan 08:00 gacha bo'lgan vaqt — kechagi tungi smenaning davomi
        prev_date = target_date - timedelta(days=1)
        _, prev_night_shift = get_shifts_for_date(prev_date)
        return shift_num == prev_night_shift


def get_schedule_badge(tabel: str, target_date: date, lang: str = "uz") -> str:
    """Xodimning ish grafigi haqida qisqa yozuv."""
    shift_num = get_employee_shift_num(tabel)
    if shift_num is None:
        if target_date.weekday() >= 5:
            return "🏖 Dam olish kuni (5-kunlik)" if lang == "uz" else "🏖 Выходной (5-дневка)"
        return "🏢 5-kunlik (09:00-18:00)" if lang == "uz" else "🏢 5-дневка (09:00-18:00)"

    day_shift, night_shift = get_shifts_for_date(target_date)
    parts = []
    if shift_num == day_shift:
        parts.append("☀️ KUN (08:00-20:00)" if lang == "uz" else "☀️ ДЕНЬ (08:00-20:00)")
    if shift_num == night_shift:
        parts.append("🌙 TUN (20:00-08:00)" if lang == "uz" else "🌙 НОЧЬ (20:00-08:00)")

    if parts:
        joined = " + ".join(parts)
        return f"🔄 {shift_num}-smena: {joined}"
    return f"🏖 Dam olish ({shift_num}-smena)" if lang == "uz" else f"🏖 Выходной ({shift_num}-смена)"


def format_daily_schedule(target_date: date, lang: str = "uz") -> str:
    """Admin yoki foydalanuvchi uchun kunlik smena grafigi matni."""
    day_shift, night_shift = get_shifts_for_date(target_date)
    is_uz = (lang == "uz")

    day_tabels = ", ".join(SHIFTS[day_shift])
    night_tabels = ", ".join(SHIFTS[night_shift])

    date_str = target_date.strftime("%d.%m.%Y")
    weekdays_uz = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    weekdays_ru = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    wd = (weekdays_uz if is_uz else weekdays_ru)[target_date.weekday()]

    if is_uz:
        lines = [
            f"📅 <b>{date_str} ({wd}) — Smena va ish grafigi</b>\n",
            f"☀️ <b>Kunduzgi smena (08:00 – 20:00):</b>",
            f"   • <b>{day_shift}-smena</b> (Tabel: {day_tabels})",
            f"\n🌙 <b>Tungi smena (20:00 – 08:00):</b>",
            f"   • <b>{night_shift}-smena</b> (Tabel: {night_tabels})",
            f"\n🏢 <b>5 kunlik ish rejimi (09:00 – 18:00):</b>",
            f"   • {'Ish kuni' if target_date.weekday() < 5 else 'Dam olish kuni (Shanba/Yakshanba)'}",
        ]
    else:
        lines = [
            f"📅 <b>{date_str} ({wd}) — График смен и работы</b>\n",
            f"☀️ <b>Дневная смена (08:00 – 20:00):</b>",
            f"   • <b>{day_shift}-смена</b> (Табель: {day_tabels})",
            f"\n🌙 <b>Ночная смена (20:00 – 08:00):</b>",
            f"   • <b>{night_shift}-смена</b> (Табель: {night_tabels})",
            f"\n🏢 <b>5-дневный график (09:00 – 18:00):</b>",
            f"   • {'Рабочий день' if target_date.weekday() < 5 else 'Выходной день'}",
        ]
    return "\n".join(lines)
