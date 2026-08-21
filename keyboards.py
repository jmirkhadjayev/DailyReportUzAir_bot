"""Klaviaturalar (matnlar i18n.py dan olinadi)."""
from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from i18n import LANG_NAMES, t

REMOVE = ReplyKeyboardRemove()


# ------------------------------------------------------------------ til

def lang_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("uz", "btn_lang_uz"), callback_data="lang:uz"),
                InlineKeyboardButton(text=t("uz", "btn_lang_ru"), callback_data="lang:ru"),
            ]
        ]
    )


# ------------------------------------------------------------------ asosiy menyular

def employee_menu(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "btn_new_report"))],
            [
                KeyboardButton(text=t(lang, "btn_my_reports")),
                KeyboardButton(text=t(lang, "btn_profile")),
            ],
            [KeyboardButton(text=t(lang, "btn_lang")), KeyboardButton(text=t(lang, "btn_help"))],
        ],
        resize_keyboard=True,
    )


def admin_menu(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t(lang, "btn_today_reports")),
                KeyboardButton(text=t(lang, "btn_missing")),
            ],
            [KeyboardButton(text=t(lang, "btn_excel")), KeyboardButton(text=t(lang, "btn_word"))],
            [
                KeyboardButton(text=t(lang, "btn_employees")),
                KeyboardButton(text=t(lang, "btn_shifts")),
            ],
            [
                KeyboardButton(text=t(lang, "btn_stats")),
                KeyboardButton(text=t(lang, "btn_broadcast")),
            ],
            [KeyboardButton(text=t(lang, "btn_lang")), KeyboardButton(text=t(lang, "btn_help"))],
        ],
        resize_keyboard=True,
    )


def cancel_kb(lang: str, skip: bool = False) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=t(lang, "btn_cancel"))]]
    if skip:
        rows.insert(0, [KeyboardButton(text=t(lang, "btn_skip"))])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


# ------------------------------------------------------------------ ro'yxatdan o'tish

def tabel_confirm_kb(lang: str, tabel: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_yes_me"), callback_data=f"tb:yes:{tabel}")],
            [InlineKeyboardButton(text=t(lang, "btn_no_me"), callback_data="tb:no")],
        ]
    )


# ------------------------------------------------------------------ hisobot

def report_date_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "btn_date_today"), callback_data="rdate:today"),
                InlineKeyboardButton(
                    text=t(lang, "btn_date_yesterday"), callback_data="rdate:yesterday"
                ),
            ],
            [InlineKeyboardButton(text=t(lang, "btn_date_other"), callback_data="rdate:custom")],
            [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="rdate:cancel")],
        ]
    )


def report_mode_kb(lang: str) -> InlineKeyboardMarkup:
    """Kun ichida ikkinchi marta yozayotganda: qo'shish yoki almashtirish."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_append"), callback_data="rmode:add")],
            [InlineKeyboardButton(text=t(lang, "btn_replace"), callback_data="rmode:replace")],
            [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="rmode:cancel")],
        ]
    )


def confirm_report_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_save_report"), callback_data="rconf:save")],
            [InlineKeyboardButton(text=t(lang, "btn_rewrite"), callback_data="rconf:restart")],
            [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="rconf:cancel")],
        ]
    )


def profile_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_lang"), callback_data="prof:lang")]
        ]
    )


# ------------------------------------------------------------------ boshliq paneli

def period_kb(lang: str, fmt: str, emp_id: int = 0) -> InlineKeyboardMarkup:
    """fmt: excel | word.  emp_id: 0 — hamma hodim, aks holda bitta hodim."""

    def cb(code: str) -> str:
        return f"per:{fmt}:{code}:{emp_id}"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "btn_p_today"), callback_data=cb("today")),
                InlineKeyboardButton(
                    text=t(lang, "btn_p_yesterday"), callback_data=cb("yesterday")
                ),
            ],
            [
                InlineKeyboardButton(text=t(lang, "btn_p_week"), callback_data=cb("week")),
                InlineKeyboardButton(text=t(lang, "btn_p_last7"), callback_data=cb("last7")),
            ],
            [
                InlineKeyboardButton(text=t(lang, "btn_p_month"), callback_data=cb("month")),
                InlineKeyboardButton(text=t(lang, "btn_p_last30"), callback_data=cb("last30")),
            ],
            [InlineKeyboardButton(text=t(lang, "btn_p_custom"), callback_data=cb("custom"))],
            [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="per:cancel:cancel:0")],
        ]
    )


def broadcast_confirm_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "btn_broadcast_send"), callback_data="bc:send")],
            [InlineKeyboardButton(text=t(lang, "btn_cancel"), callback_data="bc:cancel")],
        ]
    )


def employees_kb(rows) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=("✅ " if r["is_active"] else "🚫 ") + r["full_name"],
                    callback_data=f"emp:rep:{r['id']}",
                )
            ]
            for r in rows
        ]
    )


def employee_card_kb(lang: str, emp_id: int, is_active: bool) -> InlineKeyboardMarkup:
    toggle_key = "btn_emp_off" if is_active else "btn_emp_on"
    toggle_action = "off" if is_active else "on"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(lang, "btn_emp_reports"), callback_data=f"emp:rep:{emp_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=t(lang, "btn_emp_excel"), callback_data=f"empx:excel:{emp_id}"
                ),
                InlineKeyboardButton(
                    text=t(lang, "btn_emp_word"), callback_data=f"empx:word:{emp_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t(lang, toggle_key), callback_data=f"emp:{toggle_action}:{emp_id}"
                )
            ],
            [InlineKeyboardButton(text=t(lang, "btn_emp_del"), callback_data=f"emp:del:{emp_id}")],
        ]
    )


def confirm_delete_kb(lang: str, emp_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(lang, "btn_del_yes"), callback_data=f"emp:delyes:{emp_id}"
                )
            ],
            [InlineKeyboardButton(text=t(lang, "btn_del_no"), callback_data=f"emp:rep:{emp_id}")],
        ]
    )


def main_menu(lang: str, is_admin_user: bool) -> ReplyKeyboardMarkup:
    return admin_menu(lang) if is_admin_user else employee_menu(lang)


__all__ = [
    "REMOVE",
    "LANG_NAMES",
    "admin_menu",
    "cancel_kb",
    "confirm_delete_kb",
    "confirm_report_kb",
    "employee_card_kb",
    "employee_menu",
    "employees_kb",
    "lang_kb",
    "main_menu",
    "period_kb",
    "profile_kb",
    "report_date_kb",
    "tabel_confirm_kb",
]
