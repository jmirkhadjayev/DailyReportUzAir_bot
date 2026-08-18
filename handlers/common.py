"""Til tanlash, /start, tabel raqami orqali ro'yxatdan o'tish, /help."""
from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, User

import database as db
import keyboards as kb
import roster
from config import ADMIN_IDS, ORG_NAME, is_admin
from filters import Btn
from flows import begin_report
from i18n import LANGS, t
from states import Registration
from utils import esc, today

router = Router(name="common")
log = logging.getLogger(__name__)


async def notify_admins(bot, text_by_lang: dict[str, str] | str) -> None:
    """Adminlarga xabar (har biriga o'z tilida)."""
    for admin_id in ADMIN_IDS:
        try:
            if isinstance(text_by_lang, str):
                text = text_by_lang
            else:
                admin_lang = db.get_lang(admin_id) or "uz"
                text = text_by_lang.get(admin_lang, text_by_lang["uz"])
            await bot.send_message(admin_id, text)
        except Exception as exc:  # bot bloklangan bo'lishi mumkin
            log.warning("Adminga (%s) xabar yuborilmadi: %s", admin_id, exc)


def help_text(lang: str, admin: bool) -> str:
    if admin:
        return t(
            lang,
            "help_admin",
            today=t(lang, "btn_today_reports"),
            missing=t(lang, "btn_missing"),
            excel=t(lang, "btn_excel"),
            word=t(lang, "btn_word"),
            employees=t(lang, "btn_employees"),
            stats=t(lang, "btn_stats"),
            lang=t(lang, "btn_lang"),
        )
    return t(
        lang,
        "help_employee",
        org=esc(ORG_NAME),
        new=t(lang, "btn_new_report"),
        my=t(lang, "btn_my_reports"),
        profile=t(lang, "btn_profile"),
        lang=t(lang, "btn_lang"),
    )


# ------------------------------------------------------------------ bekor qilish

@router.message(Btn("btn_cancel"))
@router.message(Command("cancel", "bekor"))
async def cancel_any(message: Message, state: FSMContext, lang: str) -> None:
    current = await state.get_state()
    await state.clear()
    text = t(lang, "cancelled") if current else t(lang, "menu")
    await message.answer(text, reply_markup=kb.main_menu(lang, is_admin(message.from_user.id)))


@router.message(Command("id"))
async def cmd_id(message: Message, lang: str) -> None:
    await message.answer(t(lang, "id_info", id=message.from_user.id))


# ------------------------------------------------------------------ til

@router.message(Command("til", "lang", "язык"))
@router.message(Btn("btn_lang"))
async def cmd_lang(message: Message) -> None:
    await message.answer(t("uz", "lang_prompt"), reply_markup=kb.lang_kb())


@router.callback_query(F.data == "prof:lang")
async def profile_lang(call: CallbackQuery) -> None:
    await call.message.answer(t("uz", "lang_prompt"), reply_markup=kb.lang_kb())
    await call.answer()


@router.callback_query(F.data.startswith("lang:"))
async def set_language(call: CallbackQuery, state: FSMContext) -> None:
    lang = call.data.split(":", 1)[1]
    if lang not in LANGS:
        await call.answer()
        return
    db.set_lang(call.from_user.id, lang)
    await call.message.edit_text(t(lang, "lang_saved"))
    await call.answer()
    await _start_flow(call.message, call.from_user, state, lang)


# ------------------------------------------------------------------ /start

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, lang: str) -> None:
    await state.clear()
    if db.get_lang(message.from_user.id) is None:
        await message.answer(t("uz", "lang_prompt"), reply_markup=kb.lang_kb())
        return
    await _start_flow(message, message.from_user, state, lang)


async def _start_flow(message: Message, user: User, state: FSMContext, lang: str) -> None:
    """Til aniqlangandan keyingi asosiy oqim."""
    if is_admin(user.id):
        await message.answer(
            t(lang, "greet_admin", name=esc(user.full_name), org=esc(ORG_NAME)),
            reply_markup=kb.admin_menu(lang),
        )
        return

    employee = db.get_employee(user.id)
    if employee and employee["is_active"]:
        await message.answer(
            t(
                lang,
                "greet_employee",
                name=esc(employee["full_name"]),
                position=esc(employee["position"]) or "—",
                btn=t(lang, "btn_new_report"),
            ),
            reply_markup=kb.employee_menu(lang),
        )
        return

    if employee and not employee["is_active"]:
        await message.answer(t(lang, "deactivated"), reply_markup=kb.REMOVE)
        return

    await state.set_state(Registration.tabel)
    await message.answer(t(lang, "ask_tabel"), reply_markup=kb.cancel_kb(lang))


@router.message(Command("help"))
@router.message(Btn("btn_help"))
async def cmd_help(message: Message, lang: str) -> None:
    admin = is_admin(message.from_user.id)
    await message.answer(help_text(lang, admin), reply_markup=kb.main_menu(lang, admin))


# ------------------------------------------------------------------ tabel raqami = parol

@router.message(Registration.tabel, F.text)
async def enter_tabel(message: Message, state: FSMContext, lang: str) -> None:
    raw = message.text.strip()
    if not raw.isdigit():
        await message.answer(t(lang, "tabel_bad_format"))
        return

    person = roster.by_tabel(raw)
    if person is None:
        await message.answer(t(lang, "tabel_not_found", tabel=esc(raw)))
        return

    owner = db.employee_by_tabel(person["tabel"])
    if owner and owner["tg_id"] != message.from_user.id:
        await message.answer(t(lang, "tabel_taken", tabel=esc(person["tabel"])))
        return

    await message.answer(
        t(
            lang,
            "tabel_card",
            name=esc(person["full_name"]),
            position=esc(person["position"]),
            tabel=esc(person["tabel"]),
        ),
        reply_markup=kb.tabel_confirm_kb(lang, person["tabel"]),
    )


@router.callback_query(F.data == "tb:no")
async def tabel_retry(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.set_state(Registration.tabel)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(t(lang, "ask_tabel"), reply_markup=kb.cancel_kb(lang))
    await call.answer()


@router.callback_query(F.data.startswith("tb:yes:"))
async def tabel_confirm(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    person = roster.by_tabel(call.data.rsplit(":", 1)[1])
    if person is None:
        await call.answer(t(lang, "toast_not_found"), show_alert=True)
        return

    owner = db.employee_by_tabel(person["tabel"])
    if owner and owner["tg_id"] != call.from_user.id:
        await call.answer(t(lang, "tabel_taken", tabel=person["tabel"]), show_alert=True)
        return

    db.add_employee(
        tg_id=call.from_user.id,
        full_name=person["full_name"],
        position=person["position"],
        phone="",
        username=call.from_user.username or "",
        tabel=person["tabel"],
    )
    employee = db.get_employee(call.from_user.id)
    await state.clear()

    await call.message.edit_text(
        t(
            lang,
            "registered",
            name=esc(person["full_name"]),
            position=esc(person["position"]),
            tabel=esc(person["tabel"]),
        )
    )
    await call.answer()

    await notify_admins(
        call.bot,
        {
            code: t(
                code,
                "admin_new_employee",
                name=esc(person["full_name"]),
                position=esc(person["position"]),
                tabel=esc(person["tabel"]),
                username=("@" + esc(call.from_user.username)) if call.from_user.username else "—",
            )
            for code in LANGS
        },
    )

    # ro'yxatdan o'tgach — to'g'ridan-to'g'ri bugungi hisobotga
    await begin_report(call.message, state, lang, employee, today())
