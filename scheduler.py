"""Avtomatik eslatmalar va boshliqqa kunlik xulosa."""
from __future__ import annotations

import logging

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import database as db
import keyboards as kb
from config import ADMIN_IDS, DIGEST_TIME, REMINDER_TIME, TZ, WORKDAYS_ONLY, parse_hhmm
from i18n import DEFAULT_LANG, t
from utils import esc, fmt_date, iso, today

log = logging.getLogger(__name__)


async def send_reminders(bot: Bot) -> None:
    """Hisobot topshirmagan hodimlarga eslatma (har biriga o'z tilida)."""
    day = iso(today())
    for employee in db.employees_without_report(day):
        lang = db.get_lang(employee["tg_id"]) or DEFAULT_LANG
        try:
            await bot.send_message(
                employee["tg_id"],
                t(lang, "reminder", date=fmt_date(day), btn=t(lang, "btn_new_report")),
                reply_markup=kb.employee_menu(lang),
            )
        except Exception as exc:
            log.warning("Eslatma yuborilmadi (%s): %s", employee["tg_id"], exc)


async def send_digest(bot: Bot) -> None:
    """Boshliqqa kunlik xulosa."""
    day = iso(today())
    rows = db.get_reports(day, day)
    missing = db.employees_without_report(day)
    total = len(db.list_employees())

    for admin_id in ADMIN_IDS:
        lang = db.get_lang(admin_id) or DEFAULT_LANG
        text = t(
            lang,
            "digest",
            date=fmt_date(day),
            done=len(rows),
            total=total,
            missing=len(missing),
        )
        if missing:
            text += "\n" + "\n".join(f"• {esc(m['full_name'])}" for m in missing[:30])
        text += t(lang, "digest_hint", excel=t(lang, "btn_excel"), word=t(lang, "btn_word"))
        try:
            await bot.send_message(admin_id, text, reply_markup=kb.admin_menu(lang))
        except Exception as exc:
            log.warning("Xulosa yuborilmadi (%s): %s", admin_id, exc)


def setup_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=TZ)
    day_of_week = "mon-fri" if WORKDAYS_ONLY else "*"

    rh, rm = parse_hhmm(REMINDER_TIME, (17, 0))
    dh, dm = parse_hhmm(DIGEST_TIME, (18, 0))

    scheduler.add_job(
        send_reminders,
        CronTrigger(day_of_week=day_of_week, hour=rh, minute=rm, timezone=TZ),
        args=[bot],
        id="reminders",
        replace_existing=True,
    )
    scheduler.add_job(
        send_digest,
        CronTrigger(day_of_week=day_of_week, hour=dh, minute=dm, timezone=TZ),
        args=[bot],
        id="digest",
        replace_existing=True,
    )
    scheduler.start()
    log.info(
        "Rejalashtiruvchi ishga tushdi: eslatma %02d:%02d, xulosa %02d:%02d (%s)",
        rh, rm, dh, dm, day_of_week,
    )
    return scheduler
