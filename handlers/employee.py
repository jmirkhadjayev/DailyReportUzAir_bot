"""Hodimlar uchun: kundalik hisobot topshirish."""
from __future__ import annotations

from datetime import timedelta

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import database as db
import keyboards as kb
from config import is_admin
from filters import Btn
from flows import FIELD_LIMIT, MAX_PAST_DAYS, ask_done, begin_report
from handlers.common import notify_admins
from i18n import LANGS, matches, t
from states import ReportForm
from utils import (
    esc,
    fmt_date,
    fmt_date_long,
    iso,
    now_time,
    parse_user_date,
    shorten,
    today,
)

router = Router(name="employee")


async def _employee_or_none(message: Message, lang: str):
    employee = db.get_employee(message.from_user.id)
    if employee is None:
        await message.answer(t(lang, "not_registered"), reply_markup=kb.REMOVE)
        return None
    if not employee["is_active"]:
        await message.answer(t(lang, "deactivated"))
        return None
    return employee


def _preview(lang: str, data: dict) -> str:
    text = t(
        lang,
        "preview",
        date=fmt_date_long(data["report_date"], lang),
        done=esc(data.get("done")),
        problems=esc(data.get("problems") or "—"),
        plans=esc(data.get("plans") or "—"),
    )
    if data.get("mode") == "add":
        text += t(lang, "append_note")
    return text


# ------------------------------------------------------------------ hisobot boshlash

@router.message(Command("hisobot", "report", "otchet"))
@router.message(Btn("btn_new_report"))
async def start_report(message: Message, state: FSMContext, lang: str) -> None:
    employee = await _employee_or_none(message, lang)
    if employee is None:
        return
    await state.clear()
    await state.set_state(ReportForm.choosing_date)
    await message.answer(t(lang, "ask_report_date"), reply_markup=kb.report_date_kb(lang))


@router.callback_query(ReportForm.choosing_date, F.data.startswith("rdate:"))
async def choose_date(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    action = call.data.split(":", 1)[1]

    if action == "cancel":
        await state.clear()
        await call.message.edit_text(t(lang, "cancelled_short"))
        await call.message.answer(t(lang, "menu"), reply_markup=kb.employee_menu(lang))
        await call.answer()
        return

    if action == "custom":
        await state.set_state(ReportForm.custom_date)
        await call.message.edit_text(t(lang, "ask_custom_date"))
        await call.message.answer(t(lang, "send_date"), reply_markup=kb.cancel_kb(lang))
        await call.answer()
        return

    day = today() if action == "today" else today() - timedelta(days=1)
    employee = db.get_employee(call.from_user.id)
    if employee is None:
        await call.answer(t(lang, "not_registered"), show_alert=True)
        return

    await call.message.edit_text(t(lang, "date_selected", date=fmt_date_long(day, lang)))
    await begin_report(call.message, state, lang, employee, day)
    await call.answer()


@router.message(ReportForm.custom_date, F.text)
async def custom_date(message: Message, state: FSMContext, lang: str) -> None:
    day = parse_user_date(message.text)
    if day is None:
        await message.answer(t(lang, "date_invalid"))
        return
    if day > today():
        await message.answer(t(lang, "date_future"))
        return
    if (today() - day).days > MAX_PAST_DAYS:
        await message.answer(t(lang, "date_too_old", days=MAX_PAST_DAYS))
        return

    employee = await _employee_or_none(message, lang)
    if employee is None:
        return
    await begin_report(message, state, lang, employee, day)


@router.callback_query(ReportForm.choosing_mode, F.data.startswith("rmode:"))
async def choose_mode(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    action = call.data.split(":", 1)[1]

    if action == "cancel":
        await state.clear()
        await call.message.edit_text(t(lang, "cancelled_short"))
        await call.message.answer(t(lang, "menu"), reply_markup=kb.employee_menu(lang))
        await call.answer()
        return

    mode = "add" if action == "add" else "replace"
    await call.message.edit_reply_markup(reply_markup=None)
    await ask_done(call.message, state, lang, mode)
    await call.answer()


@router.message(ReportForm.done, F.text)
async def form_done(message: Message, state: FSMContext, lang: str) -> None:
    text = message.text.strip()
    if len(text) < 5:
        await message.answer(t(lang, "done_too_short"))
        return
    await state.update_data(done=text[:FIELD_LIMIT])
    await state.set_state(ReportForm.problems)
    await message.answer(
        t(lang, "ask_problems", skip=t(lang, "btn_skip")),
        reply_markup=kb.cancel_kb(lang, skip=True),
    )


@router.message(ReportForm.problems, F.text)
async def form_problems(message: Message, state: FSMContext, lang: str) -> None:
    value = "" if matches("btn_skip", message.text) else message.text.strip()[:FIELD_LIMIT]
    await state.update_data(problems=value)
    await state.set_state(ReportForm.plans)
    await message.answer(
        t(lang, "ask_plans", skip=t(lang, "btn_skip")),
        reply_markup=kb.cancel_kb(lang, skip=True),
    )


@router.message(ReportForm.plans, F.text)
async def form_plans(message: Message, state: FSMContext, lang: str) -> None:
    value = "" if matches("btn_skip", message.text) else message.text.strip()[:FIELD_LIMIT]
    await state.update_data(plans=value)
    await state.set_state(ReportForm.confirm)
    data = await state.get_data()
    await message.answer(t(lang, "check_report"), reply_markup=kb.REMOVE)
    await message.answer(_preview(lang, data), reply_markup=kb.confirm_report_kb(lang))


@router.callback_query(ReportForm.confirm, F.data.startswith("rconf:"))
async def confirm_report(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    action = call.data.split(":", 1)[1]
    data = await state.get_data()

    if action == "cancel":
        await state.clear()
        await call.message.edit_text(t(lang, "report_cancelled"))
        await call.message.answer(t(lang, "menu"), reply_markup=kb.employee_menu(lang))
        await call.answer()
        return

    if action == "restart":
        await call.message.edit_text(
            t(lang, "rewrite_intro", date=fmt_date(data["report_date"]))
        )
        await ask_done(call.message, state, lang, data.get("mode", "new"))
        await call.answer()
        return

    employee = db.get_employee_by_id(data["employee_id"])
    fields = dict(
        employee_id=data["employee_id"],
        report_date=data["report_date"],
        done=data.get("done", ""),
        problems=data.get("problems", ""),
        plans=data.get("plans", ""),
    )

    appended = False
    if data.get("mode") == "add":
        appended = db.append_report(**fields) == "appended"
        is_new = not appended
    else:
        is_new = db.upsert_report(**fields)
    await state.clear()

    if appended:
        result_text = t(
            lang,
            "saved_appended",
            date=fmt_date_long(data["report_date"], lang),
            time=now_time(),
        )
    else:
        result_text = t(
            lang,
            "saved_new" if is_new else "saved_updated",
            date=fmt_date_long(data["report_date"], lang),
        )
    await call.message.edit_text(result_text)
    await call.message.answer(t(lang, "menu"), reply_markup=kb.employee_menu(lang))
    await call.answer(t(lang, "saved_toast"))

    if appended:
        title_key = "admin_append_report"
    else:
        title_key = "admin_new_report" if is_new else "admin_upd_report"

    await notify_admins(
        call.bot,
        {
            code: t(code, title_key)
            + t(
                code,
                "admin_report_body",
                name=esc(employee["full_name"]),
                position=esc(employee["position"]) or "—",
                date=fmt_date_long(data["report_date"], code),
                done=esc(shorten(data.get("done", ""), 900)),
                problems=esc(shorten(data.get("problems", ""), 500)) or "—",
                plans=esc(shorten(data.get("plans", ""), 500)) or "—",
            )
            for code in LANGS
        },
    )


# ------------------------------------------------------------------ boshqa bo'limlar

@router.message(Btn("btn_my_reports"))
async def my_reports(message: Message, lang: str) -> None:
    employee = await _employee_or_none(message, lang)
    if employee is None:
        return
    rows = db.last_reports_of_employee(employee["id"], limit=7)
    if not rows:
        await message.answer(t(lang, "no_reports"), reply_markup=kb.employee_menu(lang))
        return

    parts = [t(lang, "my_reports_title", count=len(rows))]
    for r in rows:
        parts.append(
            f"\n🗓 <b>{fmt_date(r['report_date'])}</b>\n"
            f"✅ {esc(shorten(r['done'], 300))}\n"
            + (f"⚠️ {esc(shorten(r['problems'], 200))}\n" if r["problems"] else "")
            + (f"📌 {esc(shorten(r['plans'], 200))}\n" if r["plans"] else "")
        )
    await message.answer("".join(parts), reply_markup=kb.employee_menu(lang))


@router.message(Btn("btn_profile"))
async def profile(message: Message, lang: str) -> None:
    employee = await _employee_or_none(message, lang)
    if employee is None:
        return
    total = len(db.last_reports_of_employee(employee["id"], limit=1000))
    has_today = db.get_report(employee["id"], iso(today())) is not None
    await message.answer(
        t(
            lang,
            "profile",
            name=esc(employee["full_name"]),
            position=esc(employee["position"]) or "—",
            tabel=esc(employee["tabel"]) or "—",
            total=total,
            today_status=t(lang, "status_done" if has_today else "status_not_done"),
        ),
        reply_markup=kb.profile_kb(lang),
    )


@router.message(F.text, ~F.text.startswith("/"))
async def fallback(message: Message, lang: str) -> None:
    """Menyudan tashqari yozilgan matnlar."""
    if is_admin(message.from_user.id):
        await message.answer(t(lang, "press_menu"), reply_markup=kb.admin_menu(lang))
        return
    employee = db.get_employee(message.from_user.id)
    if employee is None:
        await message.answer(t(lang, "not_registered"))
        return
    await message.answer(
        t(lang, "press_report_btn", btn=t(lang, "btn_new_report")),
        reply_markup=kb.employee_menu(lang),
    )
