"""Boshqarma boshlig'i uchun: ko'rish, statistika, Excel/Word yuklab olish."""
from __future__ import annotations

import asyncio
from datetime import date

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message

import database as db
import keyboards as kb
import roster
from config import ORG_NAME
from exporters import build_excel, build_word
from filters import Btn, IsAdmin
from i18n import t
from states import ExportForm
from utils import (
    esc,
    fmt_date,
    fmt_date_long,
    iso,
    parse_period_input,
    period_title,
    resolve_period,
    safe_filename,
    shorten,
    today,
)

router = Router(name="admin")
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


async def send_long(message: Message, text: str, reply_markup=None) -> None:
    """Uzun matnni Telegram cheklovi (4096) bo'yicha bo'lib yuboradi."""
    limit = 3800
    chunks: list[str] = []
    current = ""
    for block in text.split("\n\n"):
        if len(current) + len(block) + 2 > limit and current:
            chunks.append(current)
            current = ""
        if len(block) > limit:
            for line in block.split("\n"):
                if len(current) + len(line) + 1 > limit and current:
                    chunks.append(current)
                    current = ""
                current += line + "\n"
        else:
            current += block + "\n\n"
    if current.strip():
        chunks.append(current)

    for i, chunk in enumerate(chunks):
        await message.answer(chunk, reply_markup=reply_markup if i == len(chunks) - 1 else None)


def _reports_text(lang: str, rows, date_from: date, date_to: date) -> str:
    period = period_title(date_from, date_to, lang)
    if not rows:
        return t(lang, "no_reports_period", period=period)

    parts = [t(lang, "reports_title", period=period, count=len(rows))]
    current_day = None
    for r in rows:
        if r["report_date"] != current_day:
            current_day = r["report_date"]
            parts.append(f"\n━━━ <b>{fmt_date_long(current_day, lang)}</b> ━━━\n")
        parts.append(
            f"\n👤 <b>{esc(r['full_name'])}</b> — <i>{esc(r['position']) or '—'}</i>\n"
            f"✅ {esc(shorten(r['done'], 700))}\n"
            + (f"⚠️ {esc(shorten(r['problems'], 400))}\n" if r["problems"] else "")
            + (f"📌 {esc(shorten(r['plans'], 400))}\n" if r["plans"] else "")
        )
    return "".join(parts)


# ------------------------------------------------------------------ ko'rish

@router.message(Btn("btn_today_reports"))
async def today_reports(message: Message, lang: str) -> None:
    day = today()
    rows = db.get_reports(iso(day), iso(day))
    missing = db.employees_without_report(iso(day))
    text = _reports_text(lang, rows, day, day)
    if missing:
        text += t(
            lang,
            "missing_block",
            count=len(missing),
            list="\n".join(f"• {esc(m['full_name'])}" for m in missing),
        )
    await send_long(message, text, reply_markup=kb.admin_menu(lang))


@router.message(Btn("btn_missing"))
async def missing_today(message: Message, lang: str) -> None:
    day = today()
    missing = db.employees_without_report(iso(day))
    total = len(db.list_employees())
    if not missing:
        await message.answer(
            t(lang, "all_submitted", total=total), reply_markup=kb.admin_menu(lang)
        )
        return
    lines = "\n".join(
        f"{i}. {esc(m['full_name'])} — <i>{esc(m['position']) or '—'}</i>"
        + (f" (@{esc(m['username'])})" if m["username"] else "")
        for i, m in enumerate(missing, start=1)
    )
    await send_long(
        message,
        t(
            lang,
            "missing_title",
            date=fmt_date(day),
            count=len(missing),
            total=total,
            list=lines,
        ),
        reply_markup=kb.admin_menu(lang),
    )


@router.message(Btn("btn_stats"))
async def stats(message: Message, lang: str) -> None:
    date_from, date_to = resolve_period("month")
    rows = db.stats_by_employee(iso(date_from), iso(date_to))
    total, active_employees = db.total_counts(iso(date_from), iso(date_to))

    lines = []
    for i, r in enumerate(rows, start=1):
        last = (
            t(lang, "stats_last", date=fmt_date(r["last_date"]))
            if r["last_date"]
            else t(lang, "stats_none")
        )
        lines.append(
            t(lang, "stats_line", i=i, name=esc(r["full_name"]), count=r["cnt"], last=last)
        )

    await send_long(
        message,
        t(
            lang,
            "stats_title",
            period=period_title(date_from, date_to, lang),
            total=total,
            active=active_employees,
            all=len(rows),
            list="\n".join(lines) if lines else t(lang, "employees_empty"),
        ),
        reply_markup=kb.admin_menu(lang),
    )


# ------------------------------------------------------------------ eksport

@router.message(Command("excel"))
@router.message(Btn("btn_excel"))
async def ask_period_excel(message: Message, state: FSMContext, lang: str) -> None:
    await state.clear()
    await message.answer(t(lang, "choose_period_excel"), reply_markup=kb.period_kb(lang, "excel"))


@router.message(Command("word"))
@router.message(Btn("btn_word"))
async def ask_period_word(message: Message, state: FSMContext, lang: str) -> None:
    await state.clear()
    await message.answer(t(lang, "choose_period_word"), reply_markup=kb.period_kb(lang, "word"))


@router.callback_query(F.data.startswith("empx:"))
async def employee_export(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    """Hodim kartasidan uning shaxsiy hisobotini yuklab olish."""
    _, fmt, raw_id = call.data.split(":", 2)
    employee = db.get_employee_by_id(int(raw_id))
    if employee is None:
        await call.answer(t(lang, "employee_not_found"), show_alert=True)
        return
    await state.clear()
    await call.message.answer(
        t(lang, "choose_period_for", name=esc(employee["full_name"])),
        reply_markup=kb.period_kb(lang, fmt, employee["id"]),
    )
    await call.answer()


@router.callback_query(F.data.startswith("per:"))
async def period_chosen(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    parts = call.data.split(":")
    fmt, code = parts[1], parts[2]
    emp_id = int(parts[3]) if len(parts) > 3 else 0

    if code == "cancel":
        await state.clear()
        await call.message.edit_text(t(lang, "cancelled_short"))
        await call.answer()
        return

    if code == "custom":
        await state.set_state(ExportForm.custom_period)
        await state.update_data(fmt=fmt, emp_id=emp_id)
        await call.message.edit_text(t(lang, "ask_custom_period"))
        await call.message.answer(t(lang, "enter_date"), reply_markup=kb.cancel_kb(lang))
        await call.answer()
        return

    date_from, date_to = resolve_period(code)
    await call.answer(t(lang, "preparing_toast"))
    await call.message.edit_text(
        t(lang, "preparing", period=period_title(date_from, date_to, lang))
    )
    await _send_export(call.message, fmt, date_from, date_to, lang, emp_id)


@router.message(ExportForm.custom_period, F.text)
async def custom_period(message: Message, state: FSMContext, lang: str) -> None:
    period = parse_period_input(message.text)
    if period is None:
        await message.answer(t(lang, "period_invalid"))
        return
    data = await state.get_data()
    await state.clear()
    date_from, date_to = period
    await message.answer(t(lang, "preparing", period=period_title(date_from, date_to, lang)))
    await _send_export(
        message, data.get("fmt", "excel"), date_from, date_to, lang, data.get("emp_id", 0)
    )


async def _send_export(
    message: Message, fmt: str, date_from: date, date_to: date, lang: str, emp_id: int = 0
) -> None:
    employee = db.get_employee_by_id(emp_id) if emp_id else None
    rows = db.get_reports(iso(date_from), iso(date_to), employee_id=emp_id or None)

    if not rows:
        await message.answer(
            t(lang, "no_reports_period", period=period_title(date_from, date_to, lang)),
            reply_markup=kb.admin_menu(lang),
        )
        return

    subject = ""
    name_part = ""
    if employee is not None:
        subject = t(
            lang,
            "doc_subject",
            name=employee["full_name"],
            position=employee["position"] or "—",
            tabel=employee["tabel"] or "—",
        )
        name_part = f"{safe_filename(employee['tabel'] or employee['full_name'])}_"

    suffix = iso(date_from) if date_from == date_to else f"{iso(date_from)}_{iso(date_to)}"
    builder = build_word if fmt == "word" else build_excel
    extension = "docx" if fmt == "word" else "xlsx"
    content = await asyncio.to_thread(builder, rows, date_from, date_to, lang, subject)
    filename = f"Hisobot_{name_part}{suffix}.{extension}"

    caption = t(
        lang,
        "doc_caption",
        org=esc(ORG_NAME),
        period=period_title(date_from, date_to, lang),
        count=len(rows),
        employees=len({r["employee_id"] for r in rows}),
    )
    if employee is not None:
        caption = f"👤 <b>{esc(employee['full_name'])}</b>\n{caption}"

    await message.answer_document(
        BufferedInputFile(content, filename=filename),
        caption=caption,
        reply_markup=kb.admin_menu(lang),
    )


# ------------------------------------------------------------------ hodimlar

@router.message(Command("hodimlar", "employees"))
@router.message(Btn("btn_employees"))
async def employees_list(message: Message, lang: str) -> None:
    rows = db.list_employees(active_only=False)
    taken = db.registered_tabels()
    not_joined = [p for p in roster.STAFF if p["tabel"] not in taken]
    pending = ""
    if not_joined:
        pending = t(
            lang,
            "not_joined",
            count=len(not_joined),
            list="\n".join(
                f"• {esc(p['full_name'])} — <i>{esc(p['position'])}</i>" for p in not_joined
            ),
        )

    if not rows:
        await send_long(
            message, t(lang, "employees_none") + pending, reply_markup=kb.admin_menu(lang)
        )
        return

    active = sum(1 for r in rows if r["is_active"])
    await message.answer(
        t(lang, "employees_title", count=len(rows), active=active),
        reply_markup=kb.employees_kb(rows),
    )
    if pending:
        await send_long(message, pending.strip(), reply_markup=kb.admin_menu(lang))


@router.callback_query(F.data.startswith("emp:"))
async def employee_actions(call: CallbackQuery, lang: str) -> None:
    _, action, raw_id = call.data.split(":", 2)
    emp_id = int(raw_id)

    if action == "off":
        db.set_employee_active(emp_id, False)
        await call.answer(t(lang, "toast_off"))
    elif action == "on":
        db.set_employee_active(emp_id, True)
        await call.answer(t(lang, "toast_on"))
    elif action == "rep":
        await call.answer()
    elif action == "del":
        employee = db.get_employee_by_id(emp_id)
        await call.message.edit_text(
            t(lang, "confirm_delete", name=esc(employee["full_name"])),
            reply_markup=kb.confirm_delete_kb(lang, emp_id),
        )
        await call.answer()
        return
    elif action == "delyes":
        employee = db.get_employee_by_id(emp_id)
        db.delete_employee(emp_id)
        await call.message.edit_text(t(lang, "deleted", name=esc(employee["full_name"])))
        await call.answer(t(lang, "toast_deleted"))
        return

    await _show_employee_card(call, emp_id, lang)


async def _show_employee_card(call: CallbackQuery, emp_id: int, lang: str) -> None:
    employee = db.get_employee_by_id(emp_id)
    if employee is None:
        await call.message.edit_text(t(lang, "employee_not_found"))
        return

    reports = db.last_reports_of_employee(emp_id, limit=5)
    parts = [
        t(
            lang,
            "employee_card",
            name=esc(employee["full_name"]),
            position=esc(employee["position"]) or "—",
            tabel=esc(employee["tabel"]) or "—",
            phone=esc(employee["phone"]) or "—",
            username=("@" + esc(employee["username"])) if employee["username"] else "—",
            status=t(lang, "status_active" if employee["is_active"] else "status_inactive"),
        )
    ]
    if reports:
        parts.append(t(lang, "last_reports_title", count=len(reports)))
        for r in reports:
            parts.append(
                f"\n🗓 <b>{fmt_date(r['report_date'])}</b>\n✅ {esc(shorten(r['done'], 350))}\n"
                + (f"⚠️ {esc(shorten(r['problems'], 200))}\n" if r["problems"] else "")
                + (f"📌 {esc(shorten(r['plans'], 200))}\n" if r["plans"] else "")
            )
    else:
        parts.append(t(lang, "no_reports_yet"))

    text = "".join(parts)
    if len(text) > 3900:
        text = text[:3900] + "…"
    await call.message.edit_text(
        text, reply_markup=kb.employee_card_kb(lang, emp_id, bool(employee["is_active"]))
    )
