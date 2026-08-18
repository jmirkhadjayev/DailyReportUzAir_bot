"""Bot sozlamalari (.env faylidan o'qiladi)."""
from __future__ import annotations

import os
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")


def _int_list(raw: str) -> list[int]:
    result = []
    for part in raw.replace(";", ",").split(","):
        part = part.strip()
        if part.lstrip("-").isdigit():
            result.append(int(part))
    return result


BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()

# Boshqarma boshlig'i (va o'rinbosarlari) ning Telegram ID raqamlari
ADMIN_IDS: list[int] = _int_list(os.getenv("ADMIN_IDS", ""))

ORG_NAME: str = os.getenv("ORG_NAME", "Boshqarma").strip()

# Hujjatlar (Excel/Word) pastida chiqadigan imzo
FOOTER_TEXT: str = os.getenv("FOOTER_TEXT", "created by mirkhadjayev.uz").strip()

# Hujjatlardagi imzo joyida turadigan boshliq F.I.Sh.
CHIEF_NAME: dict[str, str] = {
    "uz": os.getenv("CHIEF_NAME", "Atabayev F.F").strip(),
    "ru": os.getenv("CHIEF_NAME_RU", "Атабаев Ф.Ф").strip(),
}


def chief_name(lang: str) -> str:
    return CHIEF_NAME.get(lang) or CHIEF_NAME["uz"]

TIMEZONE_NAME: str = os.getenv("TIMEZONE", "Asia/Tashkent").strip()
TZ = ZoneInfo(TIMEZONE_NAME)

# Hodimlarga eslatma yuboriladigan vaqt (HH:MM)
REMINDER_TIME: str = os.getenv("REMINDER_TIME", "17:00").strip()
# Boshliqqa kunlik xulosa yuboriladigan vaqt (HH:MM)
DIGEST_TIME: str = os.getenv("DIGEST_TIME", "18:00").strip()
# Eslatma faqat ish kunlari yuborilsinmi
WORKDAYS_ONLY: bool = os.getenv("WORKDAYS_ONLY", "true").strip().lower() in {"1", "true", "yes", "ha"}

# Ma'lumotlar bazasi. Render/VPS da doimiy diskka yo'naltirish uchun:
#   DB_PATH=/var/data/reports.db
DB_PATH = Path(os.getenv("DB_PATH", DATA_DIR / "reports.db"))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Shtat ro'yxati fayli (GitHubga tushmaydi — .gitignore da).
# Render da uni "Secret File" sifatida yuklab, shu yerga yo'naltiring:
#   STAFF_FILE=/etc/secrets/staff.json
STAFF_FILE = Path(os.getenv("STAFF_FILE", BASE_DIR / "staff.json"))


def is_admin(tg_id: int) -> bool:
    return tg_id in ADMIN_IDS


def parse_hhmm(value: str, default: tuple[int, int]) -> tuple[int, int]:
    try:
        hh, mm = value.split(":")
        return int(hh), int(mm)
    except Exception:
        return default
