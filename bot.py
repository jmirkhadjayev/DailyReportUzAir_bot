"""Kundalik hisobot boti — ishga tushirish nuqtasi."""
from __future__ import annotations

import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from aiohttp import web
import database as db
from config import ADMIN_IDS, BOT_TOKEN, ORG_NAME, TIMEZONE_NAME
from handlers import setup_routers
from middlewares import LanguageMiddleware
from scheduler import setup_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
log = logging.getLogger("dailyreport")

# Render/Railway kabi xizmatlar ochiq port talab qiladi. PORT ni ular beradi,
# bo'lmasa 8080 ishlatiladi. Bot polling rejimida ishlaydi, bu server faqat
# "tirikman" deb javob berish uchun kerak.
PORT = int(os.environ.get("PORT", 8080))


async def handle(_request: web.Request) -> web.Response:
    return web.Response(text="Bot is running!")


async def start_web_server() -> web.AppRunner:
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    log.info("HTTP server ishga tushdi: 0.0.0.0:%s", PORT)
    return runner


COMMANDS = {
    "uz": [
        ("start", "Boshlash / bosh menyu"),
        ("hisobot", "Kundalik hisobot topshirish"),
        ("til", "Tilni o'zgartirish"),
        ("help", "Yordam"),
        ("cancel", "Amalni bekor qilish"),
        ("id", "Telegram ID raqamim"),
    ],
    "ru": [
        ("start", "Начать / главное меню"),
        ("hisobot", "Сдать ежедневный отчёт"),
        ("til", "Сменить язык"),
        ("help", "Помощь"),
        ("cancel", "Отменить действие"),
        ("id", "Мой Telegram ID"),
    ],
}

ADMIN_EXTRA = {
    "uz": [
        ("excel", "Excel faylni yuklab olish"),
        ("word", "Word faylni yuklab olish"),
        ("hodimlar", "Hodimlar ro'yxati"),
    ],
    "ru": [
        ("excel", "Скачать файл Excel"),
        ("word", "Скачать файл Word"),
        ("hodimlar", "Список сотрудников"),
    ],
}


def _commands(lang: str, admin: bool) -> list[BotCommand]:
    items = COMMANDS[lang] + (ADMIN_EXTRA[lang] if admin else [])
    return [BotCommand(command=cmd, description=desc) for cmd, desc in items]


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(_commands("uz", False), scope=BotCommandScopeDefault())
    await bot.set_my_commands(
        _commands("ru", False), scope=BotCommandScopeDefault(), language_code="ru"
    )
    for admin_id in ADMIN_IDS:
        lang = db.get_lang(admin_id) or "uz"
        try:
            await bot.set_my_commands(
                _commands(lang, True), scope=BotCommandScopeChat(chat_id=admin_id)
            )
        except Exception as exc:
            log.warning("Admin buyruqlari o'rnatilmadi (%s): %s", admin_id, exc)


async def main() -> None:
    if not BOT_TOKEN:
        log.error(
            "BOT_TOKEN topilmadi! .env.example faylini .env deb nusxalang va "
            "@BotFather bergan tokenni yozing."
        )
        sys.exit(1)
    if not ADMIN_IDS:
        log.warning(
            "ADMIN_IDS bo'sh — boshqaruv paneli hech kimga ochilmaydi. "
            "Botga /id yuboring va raqamni .env faylidagi ADMIN_IDS ga yozing."
        )

    db.init_db()
    log.info("Tashkilot: %s | Vaqt mintaqasi: %s", ORG_NAME, TIMEZONE_NAME)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.update.outer_middleware(LanguageMiddleware())
    dispatcher.include_router(setup_routers())

    try:
        me = await bot.get_me()
    except TelegramUnauthorizedError:
        log.error("BOT_TOKEN noto'g'ri. @BotFather dan yangi token oling va .env fayliga yozing.")
        await bot.session.close()
        sys.exit(1)

    await set_commands(bot)
    scheduler = setup_scheduler(bot)
    runner = await start_web_server()   # Render portni aniqlashi uchun
    log.info("Bot ishga tushdi: @%s", me.username)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dispatcher.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)
        await runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Bot to'xtatildi.")
