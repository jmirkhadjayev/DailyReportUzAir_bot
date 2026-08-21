"""Avtomatik eslatmalar va boshliqqa kunlik xulosa."""
from __future__ import annotations

import logging
from datetime import datetime

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import database as db
import keyboards as kb
import shifts
from config import ADMIN_IDS, DIGEST_TIME, TZ, parse_hhmm, reminder_times
from i18n import DEFAULT_LANG, t
from utils import esc, fmt_date, iso, today

log = logging.getLogger(__name__)


async def send_reminders(bot: Bot) -> None:
    """Hisobot topshirmagan hodimlarga eslatma (har biriga o'z tilida va o'z ish vaqtida)."""
    now_dt = datetime.now(TZ)
    current_date = now_dt.date()
    current_time = now_dt.time()
    day_str = iso(current_date)

    for employee in db.employees_without_report(day_str):
        # Faqat ayni vaqtda ishda / navbatchilikda bo'lgan xodimlarga eslatma boradi
        if not shifts.is_on_duty(employee["tabel"], current_date, current_time):
            continue

        lang = db.get_lang(employee["tg_id"]) or DEFAULT_LANG
        try:
            await bot.send_message(
                employee["tg_id"],
                t(lang, "reminder", date=fmt_date(day_str), btn=t(lang, "btn_new_report")),
                reply_markup=kb.employee_menu(lang),
            )
        except Exception as exc:
            log.warning("Eslatma yuborilmadi (%s): %s", employee["tg_id"], exc)


async def send_digest(bot: Bot) -> None:
    """Boshliqqa kunlik xulosa."""
    day = today()
    day_str = iso(day)
    rows = db.get_reports(day_str, day_str)
    all_missing = db.employees_without_report(day_str)

    # Faqat shu kuni ishlashi kerak bo'lgan xodimlar
    missing = [m for m in all_missing if shifts.is_on_duty(m["tabel"], day, check_time=None)]
    expected_employees = [e for e in db.list_employees() if shifts.is_on_duty(e["tabel"], day, check_time=None)]
    total = len(expected_employees) or len(db.list_employees())

    for admin_id in ADMIN_IDS:
        lang = db.get_lang(admin_id) or DEFAULT_LANG
        text = t(
            lang,
            "digest",
            date=fmt_date(day_str),
            done=len(rows),
            total=total,
            missing=len(missing),
        )
        if missing:
            text += "\n" + "\n".join(
                f"• {esc(m['full_name'])} <i>({shifts.get_schedule_badge(m['tabel'], day, lang)})</i>"
                for m in missing[:30]
            )
        text += t(lang, "digest_hint", excel=t(lang, "btn_excel"), word=t(lang, "btn_word"))
        try:
            await bot.send_message(admin_id, text, reply_markup=kb.admin_menu(lang))
        except Exception as exc:
            log.warning("Xulosa yuborilmadi (%s): %s", admin_id, exc)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=TZ)

    # Kunduzgi eslatmalar (sozlamadagi vaqtlar: masalan 08:00, 12:00, 16:00, 20:00)
    times = reminder_times()
    for index, (hour, minute) in enumerate(times, start=1):
        scheduler.add_job(
            send_reminders,
            CronTrigger(day_of_week="*", hour=hour, minute=minute, timezone=TZ),
            args=[bot],
            id=f"reminder_{index}",
            replace_existing=True,
        )

    # Tungi smenalar uchun qo'shimcha eslatmalar (00:00 va 04:00)
    night_times = [(0, 0), (4, 0)]
    for index, (hour, minute) in enumerate(night_times, start=100):
        scheduler.add_job(
            send_reminders,
            CronTrigger(day_of_week="*", hour=hour, minute=minute, timezone=TZ),
            args=[bot],
            id=f"night_reminder_{index}",
            replace_existing=True,
        )

    # Boshliqqa kunlik xulosa
    dh, dm = parse_hhmm(DIGEST_TIME, (23, 59))
    scheduler.add_job(
        send_digest,
        CronTrigger(day_of_week="*", hour=dh, minute=dm, timezone=TZ),
        args=[bot],
        id="digest",
        replace_existing=True,
    )

    scheduler.start()
    log.info(
        "Rejalashtiruvchi: eslatmalar (kunduzgi: %s, tungi: %s) | kunlik xulosa %02d:%02d",
        ", ".join(f"{h:02d}:{m:02d}" for h, m in times),
        ", ".join(f"{h:02d}:{m:02d}" for h, m in night_times),
        dh, dm,
    )
    return scheduler
