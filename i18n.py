"""Ko'p tillilik — barcha matnlar shu yerda (o'zbekcha / ruscha).

Yangi matn qo'shish: TEXTS ga kalit qo'shing va ikkala tilga tarjimasini yozing.
"""
from __future__ import annotations

LANGS = ("uz", "ru")
DEFAULT_LANG = "uz"

LANG_NAMES = {"uz": "O'zbekcha", "ru": "Русский"}

TEXTS: dict[str, dict[str, str]] = {
    # ------------------------------------------------------------ til
    "lang_prompt": {
        "uz": "🌐 <b>Tilni tanlang / Выберите язык</b>",
        "ru": "🌐 <b>Tilni tanlang / Выберите язык</b>",
    },
    "btn_lang_uz": {"uz": "🇺🇿 O'zbekcha", "ru": "🇺🇿 O'zbekcha"},
    "btn_lang_ru": {"uz": "🇷🇺 Русский", "ru": "🇷🇺 Русский"},
    "lang_saved": {"uz": "✅ Til: O'zbekcha", "ru": "✅ Язык: Русский"},

    # ------------------------------------------------------------ menyu tugmalari
    "btn_new_report": {"uz": "📝 Hisobot topshirish", "ru": "📝 Сдать отчёт"},
    "btn_my_reports": {"uz": "📋 Mening hisobotlarim", "ru": "📋 Мои отчёты"},
    "btn_profile": {"uz": "👤 Profilim", "ru": "👤 Мой профиль"},
    "btn_help": {"uz": "ℹ️ Yordam", "ru": "ℹ️ Помощь"},
    "btn_lang": {"uz": "🌐 Til", "ru": "🌐 Язык"},
    "btn_today_reports": {"uz": "📊 Bugungi hisobotlar", "ru": "📊 Отчёты за сегодня"},
    "btn_missing": {"uz": "⏳ Topshirmaganlar", "ru": "⏳ Не сдали"},
    "btn_excel": {"uz": "📥 Excel (.xlsx)", "ru": "📥 Excel (.xlsx)"},
    "btn_word": {"uz": "📥 Word (.docx)", "ru": "📥 Word (.docx)"},
    "btn_employees": {"uz": "👥 Hodimlar", "ru": "👥 Сотрудники"},
    "btn_stats": {"uz": "📈 Statistika", "ru": "📈 Статистика"},
    "btn_skip": {"uz": "⏭ O'tkazib yuborish", "ru": "⏭ Пропустить"},
    "btn_cancel": {"uz": "❌ Bekor qilish", "ru": "❌ Отмена"},

    # ------------------------------------------------------------ umumiy
    "menu": {"uz": "Bosh menyu.", "ru": "Главное меню."},
    "cancelled": {"uz": "❌ Amal bekor qilindi.", "ru": "❌ Действие отменено."},
    "greet_admin": {
        "uz": "👋 Assalomu alaykum, <b>{name}</b>!\n\n"
              "«{org}» kundalik hisobotlar tizimi.\nMenyudan kerakli bo'limni tanlang.",
        "ru": "👋 Здравствуйте, <b>{name}</b>!\n\n"
              "Система ежедневных отчётов «{org}».\nВыберите раздел в меню.",
    },
    "greet_employee": {
        "uz": "👋 Assalomu alaykum, <b>{name}</b>!\n💼 {position}\n\n"
              "Kundalik hisobotni topshirish uchun «{btn}» tugmasini bosing.",
        "ru": "👋 Здравствуйте, <b>{name}</b>!\n💼 {position}\n\n"
              "Нажмите «{btn}», чтобы сдать ежедневный отчёт.",
    },
    "deactivated": {
        "uz": "🚫 Hisobingiz vaqtincha faolsizlantirilgan.\nBoshqarma boshlig'iga murojaat qiling.",
        "ru": "🚫 Ваша учётная запись временно отключена.\nОбратитесь к начальнику управления.",
    },
    "not_registered": {
        "uz": "Siz hali ro'yxatdan o'tmagansiz. /start buyrug'ini yuboring.",
        "ru": "Вы ещё не зарегистрированы. Отправьте команду /start.",
    },
    "id_info": {
        "uz": "🆔 Sizning Telegram ID raqamingiz: <code>{id}</code>\n\n"
              "Uni <code>.env</code> faylidagi <code>ADMIN_IDS</code> qatoriga yozsangiz, "
              "boshqaruv paneli ochiladi.",
        "ru": "🆔 Ваш Telegram ID: <code>{id}</code>\n\n"
              "Укажите его в строке <code>ADMIN_IDS</code> файла <code>.env</code>, "
              "чтобы открылась панель руководителя.",
    },
    "press_menu": {
        "uz": "Quyidagi menyudan tanlang 👇",
        "ru": "Выберите пункт меню 👇",
    },
    "press_report_btn": {
        "uz": "Hisobot topshirish uchun «{btn}» tugmasini bosing 👇",
        "ru": "Нажмите «{btn}», чтобы сдать отчёт 👇",
    },

    # ------------------------------------------------------------ ro'yxatdan o'tish (tabel = parol)
    "ask_tabel": {
        "uz": "🔢 <b>Tabel raqamingizni kiriting.</b>\n\n"
              "U parol vazifasini bajaradi: raqamni kiritishingiz bilan "
              "F.I.Sh. va lavozimingiz avtomatik aniqlanadi.\n\n<i>Masalan: 1234</i>",
        "ru": "🔢 <b>Введите свой табельный номер.</b>\n\n"
              "Он работает как пароль: по нему автоматически определятся "
              "Ф.И.О. и должность.\n\n<i>Например: 1234</i>",
    },
    "tabel_bad_format": {
        "uz": "⚠️ Tabel raqami faqat raqamlardan iborat bo'lishi kerak. Masalan: <code>1234</code>",
        "ru": "⚠️ Табельный номер состоит только из цифр. Например: <code>1234</code>",
    },
    "tabel_not_found": {
        "uz": "❌ <b>{tabel}</b> — bunday tabel raqami shtat ro'yxatida yo'q.\n\n"
              "Raqamni tekshirib qayta kiriting yoki boshqarma boshlig'iga murojaat qiling.",
        "ru": "❌ <b>{tabel}</b> — такого табельного номера нет в штатном списке.\n\n"
              "Проверьте номер или обратитесь к начальнику управления.",
    },
    "tabel_taken": {
        "uz": "🚫 <b>{tabel}</b> raqami allaqachon boshqa Telegram akkauntga biriktirilgan.\n\n"
              "Boshqarma boshlig'iga murojaat qiling.",
        "ru": "🚫 Номер <b>{tabel}</b> уже привязан к другому аккаунту Telegram.\n\n"
              "Обратитесь к начальнику управления.",
    },
    "tabel_card": {
        "uz": "🔎 <b>Topildi</b>\n\n"
              "👤 F.I.Sh.: <b>{name}</b>\n💼 Lavozim: <b>{position}</b>\n"
              "🔢 Tabel №: <code>{tabel}</code>\n\nBu sizmi?",
        "ru": "🔎 <b>Найдено</b>\n\n"
              "👤 Ф.И.О.: <b>{name}</b>\n💼 Должность: <b>{position}</b>\n"
              "🔢 Таб. №: <code>{tabel}</code>\n\nЭто вы?",
    },
    "btn_yes_me": {"uz": "✅ Ha, bu menman", "ru": "✅ Да, это я"},
    "btn_no_me": {"uz": "🔁 Yo'q, boshqa raqam", "ru": "🔁 Нет, другой номер"},
    "registered": {
        "uz": "🎉 <b>Ro'yxatdan o'tdingiz!</b>\n\n👤 {name}\n💼 {position}\n🔢 Tabel №: {tabel}\n\n"
              "Endi kundalik hisobotni to'ldiramiz 👇",
        "ru": "🎉 <b>Вы зарегистрированы!</b>\n\n👤 {name}\n💼 {position}\n🔢 Таб. №: {tabel}\n\n"
              "Теперь заполним ежедневный отчёт 👇",
    },
    "admin_new_employee": {
        "uz": "🆕 <b>Yangi hodim ro'yxatdan o'tdi</b>\n\n"
              "👤 {name}\n💼 {position}\n🔢 Tabel №: {tabel}\n🔗 {username}",
        "ru": "🆕 <b>Зарегистрировался новый сотрудник</b>\n\n"
              "👤 {name}\n💼 {position}\n🔢 Таб. №: {tabel}\n🔗 {username}",
    },

    # ------------------------------------------------------------ hisobot
    "ask_report_date": {"uz": "Hisobot qaysi kun uchun?", "ru": "За какой день отчёт?"},
    "btn_date_today": {"uz": "📅 Bugun", "ru": "📅 Сегодня"},
    "btn_date_yesterday": {"uz": "📅 Kecha", "ru": "📅 Вчера"},
    "btn_date_other": {"uz": "🗓 Boshqa sana", "ru": "🗓 Другая дата"},
    "date_selected": {"uz": "🗓 Tanlangan sana: <b>{date}</b>", "ru": "🗓 Выбранная дата: <b>{date}</b>"},
    "ask_custom_date": {
        "uz": "🗓 Sanani kiriting: <code>KK.OO.YYYY</code>\n\n<i>Masalan: 15.08.2026</i>",
        "ru": "🗓 Введите дату: <code>ДД.ММ.ГГГГ</code>\n\n<i>Например: 15.08.2026</i>",
    },
    "send_date": {"uz": "Sanani yuboring:", "ru": "Отправьте дату:"},
    "date_invalid": {
        "uz": "⚠️ Sana noto'g'ri. Namuna: <code>15.08.2026</code>",
        "ru": "⚠️ Неверная дата. Пример: <code>15.08.2026</code>",
    },
    "date_future": {
        "uz": "⚠️ Kelajakdagi sana uchun hisobot topshirib bo'lmaydi.",
        "ru": "⚠️ Нельзя сдать отчёт за будущую дату.",
    },
    "date_too_old": {
        "uz": "⚠️ Faqat oxirgi {days} kun ichidagi sana tanlanadi.",
        "ru": "⚠️ Доступны только последние {days} дней.",
    },
    "ask_done": {
        "uz": "1️⃣ <b>Bajarilgan ishlaringizni</b> yozing.\n"
              "Har bir ishni yangi qatordan yozsangiz, hujjat chiroyli chiqadi.\n\n"
              "<i>Masalan:\n— 12 ta hujjat ko'rib chiqildi\n— Yig'ilishda qatnashildi</i>",
        "ru": "1️⃣ Напишите <b>выполненные работы</b>.\n"
              "Каждую — с новой строки, тогда документ будет аккуратным.\n\n"
              "<i>Например:\n— рассмотрено 12 документов\n— участие в совещании</i>",
    },
    "done_too_short": {
        "uz": "⚠️ Iltimos, bajarilgan ishlarni batafsilroq yozing.",
        "ru": "⚠️ Пожалуйста, опишите выполненные работы подробнее.",
    },
    "report_exists_choice": {
        "uz": "📄 <b>{date}</b> uchun hisobotingiz allaqachon bor:\n\n<i>{preview}</i>\n\n"
              "Nima qilamiz?",
        "ru": "📄 Отчёт за <b>{date}</b> уже есть:\n\n<i>{preview}</i>\n\nЧто делаем?",
    },
    "btn_append": {"uz": "➕ Davomini qo'shish", "ru": "➕ Дополнить"},
    "btn_replace": {"uz": "♻️ Butunlay almashtirish", "ru": "♻️ Заменить полностью"},
    "append_note": {
        "uz": "\n\n➕ <i>Yozganingiz bugungi hisobotga vaqti bilan qo'shiladi — "
              "eski matn o'chmaydi.</i>",
        "ru": "\n\n➕ <i>Написанное добавится к сегодняшнему отчёту с отметкой времени — "
              "старый текст сохранится.</i>",
    },
    "saved_appended": {
        "uz": "✅ <b>Hisobotga qo'shildi!</b>\n\n🗓 {date}\n🕐 {time}\nRahmat! 💪",
        "ru": "✅ <b>Добавлено в отчёт!</b>\n\n🗓 {date}\n🕐 {time}\nСпасибо! 💪",
    },
    "admin_append_report": {
        "uz": "➕ <b>Hisobotga qo'shimcha</b>", "ru": "➕ <b>Дополнение к отчёту</b>",
    },
    "report_exists": {
        "uz": "\n\n⚠️ <b>{date}</b> uchun hisobotingiz allaqachon bor. "
              "Yangisini yozsangiz, eskisi yangilanadi.\n<i>Avvalgi matn: {preview}</i>",
        "ru": "\n\n⚠️ Отчёт за <b>{date}</b> уже есть. "
              "Новый заменит старый.\n<i>Предыдущий текст: {preview}</i>",
    },
    "ask_problems": {
        "uz": "2️⃣ <b>Muammo va takliflaringiz</b> bormi?\nBo'lmasa — «{skip}» tugmasini bosing.",
        "ru": "2️⃣ Есть ли <b>проблемы и предложения</b>?\nЕсли нет — нажмите «{skip}».",
    },
    "ask_plans": {
        "uz": "3️⃣ <b>Ertangi kun rejalaringizni</b> yozing.\nBo'lmasa — «{skip}» tugmasini bosing.",
        "ru": "3️⃣ Напишите <b>планы на завтра</b>.\nЕсли нет — нажмите «{skip}».",
    },
    "check_report": {"uz": "Tekshirib chiqing 👇", "ru": "Проверьте отчёт 👇"},
    "preview": {
        "uz": "📄 <b>Hisobot ko'rinishi</b>\n🗓 Sana: <b>{date}</b>\n\n"
              "1️⃣ <b>Bajarilgan ishlar:</b>\n{done}\n\n"
              "2️⃣ <b>Muammo va takliflar:</b>\n{problems}\n\n"
              "3️⃣ <b>Ertangi rejalar:</b>\n{plans}\n\nHammasi to'g'rimi?",
        "ru": "📄 <b>Предпросмотр отчёта</b>\n🗓 Дата: <b>{date}</b>\n\n"
              "1️⃣ <b>Выполненные работы:</b>\n{done}\n\n"
              "2️⃣ <b>Проблемы и предложения:</b>\n{problems}\n\n"
              "3️⃣ <b>Планы на завтра:</b>\n{plans}\n\nВсё верно?",
    },
    "btn_save_report": {"uz": "✅ Tasdiqlash va yuborish", "ru": "✅ Подтвердить и отправить"},
    "btn_rewrite": {"uz": "✏️ Qaytadan yozish", "ru": "✏️ Написать заново"},
    "report_cancelled": {
        "uz": "❌ Hisobot bekor qilindi, saqlanmadi.",
        "ru": "❌ Отчёт отменён и не сохранён.",
    },
    "rewrite_intro": {
        "uz": "✏️ Qaytadan yozamiz. Sana: <b>{date}</b>",
        "ru": "✏️ Пишем заново. Дата: <b>{date}</b>",
    },
    "ask_done_short": {
        "uz": "1️⃣ <b>Bajarilgan ishlarni</b> yozing:",
        "ru": "1️⃣ Напишите <b>выполненные работы</b>:",
    },
    "saved_new": {
        "uz": "✅ <b>Hisobot qabul qilindi!</b>\n\n🗓 {date}\nRahmat, sizga omad! 💪",
        "ru": "✅ <b>Отчёт принят!</b>\n\n🗓 {date}\nСпасибо, удачи! 💪",
    },
    "saved_updated": {
        "uz": "✅ <b>Hisobot yangilandi!</b>\n\n🗓 {date}",
        "ru": "✅ <b>Отчёт обновлён!</b>\n\n🗓 {date}",
    },
    "saved_toast": {"uz": "Saqlandi ✅", "ru": "Сохранено ✅"},
    "admin_new_report": {
        "uz": "🆕 <b>Yangi hisobot</b>", "ru": "🆕 <b>Новый отчёт</b>",
    },
    "admin_upd_report": {
        "uz": "♻️ <b>Hisobot yangilandi</b>", "ru": "♻️ <b>Отчёт обновлён</b>",
    },
    "admin_report_body": {
        "uz": "\n\n👤 <b>{name}</b>\n💼 {position}\n🗓 {date}\n\n"
              "1️⃣ <b>Bajarilgan ishlar:</b>\n{done}\n\n"
              "2️⃣ <b>Muammolar:</b>\n{problems}\n\n3️⃣ <b>Rejalar:</b>\n{plans}",
        "ru": "\n\n👤 <b>{name}</b>\n💼 {position}\n🗓 {date}\n\n"
              "1️⃣ <b>Выполненные работы:</b>\n{done}\n\n"
              "2️⃣ <b>Проблемы:</b>\n{problems}\n\n3️⃣ <b>Планы:</b>\n{plans}",
    },

    # ------------------------------------------------------------ hodim bo'limlari
    "my_reports_title": {
        "uz": "📋 <b>Oxirgi {count} ta hisobotingiz</b>\n",
        "ru": "📋 <b>Ваши последние отчёты: {count}</b>\n",
    },
    "no_reports": {"uz": "📭 Sizda hali hisobot yo'q.", "ru": "📭 У вас пока нет отчётов."},
    "profile": {
        "uz": "👤 <b>Profilingiz</b>\n\nF.I.Sh.: <b>{name}</b>\n💼 Lavozim: {position}\n"
              "🔢 Tabel №: {tabel}\n📊 Jami hisobotlar: <b>{total}</b> ta\n"
              "🗓 Bugungi hisobot: {today_status}",
        "ru": "👤 <b>Ваш профиль</b>\n\nФ.И.О.: <b>{name}</b>\n💼 Должность: {position}\n"
              "🔢 Таб. №: {tabel}\n📊 Всего отчётов: <b>{total}</b>\n"
              "🗓 Отчёт за сегодня: {today_status}",
    },
    "status_done": {"uz": "✅ topshirilgan", "ru": "✅ сдан"},
    "status_not_done": {"uz": "❌ topshirilmagan", "ru": "❌ не сдан"},

    # ------------------------------------------------------------ boshliq paneli
    "reports_title": {
        "uz": "📊 <b>Hisobotlar — {period}</b>\nJami: {count} ta\n",
        "ru": "📊 <b>Отчёты — {period}</b>\nВсего: {count}\n",
    },
    "no_reports_period": {
        "uz": "📭 <b>{period}</b> uchun hisobot topilmadi.",
        "ru": "📭 За период <b>{period}</b> отчётов нет.",
    },
    "missing_block": {
        "uz": "\n\n⏳ <b>Topshirmaganlar ({count} ta):</b>\n{list}",
        "ru": "\n\n⏳ <b>Не сдали ({count}):</b>\n{list}",
    },
    "all_submitted": {
        "uz": "🎉 Barcha hodimlar ({total} ta) bugungi hisobotni topshirgan!",
        "ru": "🎉 Все сотрудники ({total}) сдали сегодняшний отчёт!",
    },
    "missing_title": {
        "uz": "⏳ <b>{date} — hisobot topshirmaganlar</b>\n{count} / {total} hodim\n\n{list}",
        "ru": "⏳ <b>{date} — не сдали отчёт</b>\n{count} / {total} сотрудников\n\n{list}",
    },
    "stats_title": {
        "uz": "📈 <b>Statistika — {period}</b>\n\nJami hisobotlar: <b>{total}</b> ta\n"
              "Hisobot topshirgan hodimlar: <b>{active}</b> / {all}\n\n{list}",
        "ru": "📈 <b>Статистика — {period}</b>\n\nВсего отчётов: <b>{total}</b>\n"
              "Сдавали отчёты: <b>{active}</b> / {all}\n\n{list}",
    },
    "stats_line": {
        "uz": "{i}. <b>{name}</b> — {count} ta ({last})",
        "ru": "{i}. <b>{name}</b> — {count} ({last})",
    },
    "stats_last": {"uz": "oxirgi: {date}", "ru": "последний: {date}"},
    "stats_none": {"uz": "hisobot yo'q", "ru": "нет отчётов"},
    "employees_empty": {"uz": "Hodimlar ro'yxati bo'sh.", "ru": "Список сотрудников пуст."},

    "choose_period_excel": {
        "uz": "📥 <b>Excel</b> uchun davrni tanlang:",
        "ru": "📥 Выберите период для <b>Excel</b>:",
    },
    "choose_period_word": {
        "uz": "📥 <b>Word</b> uchun davrni tanlang:",
        "ru": "📥 Выберите период для <b>Word</b>:",
    },
    "btn_p_today": {"uz": "Bugun", "ru": "Сегодня"},
    "btn_p_yesterday": {"uz": "Kecha", "ru": "Вчера"},
    "btn_p_week": {"uz": "Shu hafta", "ru": "Эта неделя"},
    "btn_p_last7": {"uz": "Oxirgi 7 kun", "ru": "Последние 7 дней"},
    "btn_p_month": {"uz": "Shu oy", "ru": "Этот месяц"},
    "btn_p_last30": {"uz": "Oxirgi 30 kun", "ru": "Последние 30 дней"},
    "btn_p_custom": {"uz": "🗓 Sanani o'zim tanlayman", "ru": "🗓 Выбрать даты"},
    "ask_custom_period": {
        "uz": "🗓 Davrni yuboring:\n\n• Bitta kun: <code>15.08.2026</code>\n"
              "• Davr: <code>01.08.2026 - 18.08.2026</code>",
        "ru": "🗓 Отправьте период:\n\n• Один день: <code>15.08.2026</code>\n"
              "• Период: <code>01.08.2026 - 18.08.2026</code>",
    },
    "enter_date": {"uz": "Sanani kiriting:", "ru": "Введите дату:"},
    "period_invalid": {
        "uz": "⚠️ Sana tushunarsiz. Namuna: <code>01.08.2026 - 18.08.2026</code>",
        "ru": "⚠️ Не удалось распознать дату. Пример: <code>01.08.2026 - 18.08.2026</code>",
    },
    "preparing": {
        "uz": "⏳ <b>{period}</b> uchun hujjat tayyorlanmoqda…",
        "ru": "⏳ Готовится документ за <b>{period}</b>…",
    },
    "preparing_toast": {"uz": "Tayyorlanmoqda…", "ru": "Готовится…"},
    "doc_caption": {
        "uz": "📄 <b>{org}</b>\nDavr: <b>{period}</b>\n"
              "Hisobotlar: <b>{count}</b> ta  |  Hodimlar: <b>{employees}</b> ta",
        "ru": "📄 <b>{org}</b>\nПериод: <b>{period}</b>\n"
              "Отчётов: <b>{count}</b>  |  Сотрудников: <b>{employees}</b>",
    },

    "employees_title": {
        "uz": "👥 <b>Botdagi hodimlar</b>\nJami: {count} ta (faol: {active})\n\n"
              "Batafsil ma'lumot uchun hodimni tanlang:",
        "ru": "👥 <b>Сотрудники в боте</b>\nВсего: {count} (активных: {active})\n\n"
              "Выберите сотрудника для подробностей:",
    },
    "employees_none": {
        "uz": "👥 Hali hech kim ro'yxatdan o'tmagan.\n\n"
              "Hodimlar botga <b>/start</b> bosib, tabel raqamini kiritishlari kerak.",
        "ru": "👥 Пока никто не зарегистрирован.\n\n"
              "Сотрудникам нужно нажать <b>/start</b> в боте и ввести табельный номер.",
    },
    "not_joined": {
        "uz": "\n\n📵 <b>Botga hali ulanmaganlar ({count} ta):</b>\n{list}",
        "ru": "\n\n📵 <b>Ещё не подключились к боту ({count}):</b>\n{list}",
    },
    "employee_card": {
        "uz": "👤 <b>{name}</b>\n💼 {position}\n🔢 Tabel №: {tabel}\n📱 {phone}\n🔗 {username}\n"
              "Holati: {status}\n",
        "ru": "👤 <b>{name}</b>\n💼 {position}\n🔢 Таб. №: {tabel}\n📱 {phone}\n🔗 {username}\n"
              "Статус: {status}\n",
    },
    "status_active": {"uz": "✅ faol", "ru": "✅ активен"},
    "status_inactive": {"uz": "🚫 faolsiz", "ru": "🚫 отключён"},
    "last_reports_title": {
        "uz": "\n📋 <b>Oxirgi {count} ta hisoboti:</b>\n",
        "ru": "\n📋 <b>Последние отчёты ({count}):</b>\n",
    },
    "no_reports_yet": {"uz": "\n📭 Hali hisobot topshirmagan.", "ru": "\n📭 Отчётов пока нет."},
    "employee_not_found": {"uz": "Hodim topilmadi.", "ru": "Сотрудник не найден."},
    "btn_emp_reports": {"uz": "📋 Oxirgi hisobotlari", "ru": "📋 Последние отчёты"},
    "btn_emp_off": {"uz": "🚫 Faolsizlantirish", "ru": "🚫 Отключить"},
    "btn_emp_on": {"uz": "✅ Faollashtirish", "ru": "✅ Включить"},
    "btn_emp_del": {"uz": "🗑 O'chirish", "ru": "🗑 Удалить"},
    "btn_del_yes": {"uz": "🗑 Ha, o'chirilsin", "ru": "🗑 Да, удалить"},
    "btn_del_no": {"uz": "↩️ Yo'q", "ru": "↩️ Нет"},
    "confirm_delete": {
        "uz": "🗑 <b>{name}</b> va uning barcha hisobotlari butunlay o'chirilsinmi?",
        "ru": "🗑 Удалить <b>{name}</b> и все его отчёты безвозвратно?",
    },
    "deleted": {"uz": "🗑 <b>{name}</b> o'chirildi.", "ru": "🗑 <b>{name}</b> удалён."},
    "toast_off": {"uz": "Faolsizlantirildi", "ru": "Отключён"},
    "toast_on": {"uz": "Faollashtirildi", "ru": "Включён"},
    "toast_deleted": {"uz": "O'chirildi", "ru": "Удалён"},
    "toast_not_found": {"uz": "Topilmadi", "ru": "Не найдено"},
    "cancelled_short": {"uz": "❌ Bekor qilindi.", "ru": "❌ Отменено."},

    # ------------------------------------------------------------ eslatmalar
    "reminder": {
        "uz": "⏰ <b>Eslatma</b>\n\nBugungi ({date}) kundalik hisobotingiz hali topshirilmagan.\n"
              "«{btn}» tugmasini bosing 👇",
        "ru": "⏰ <b>Напоминание</b>\n\nВаш ежедневный отчёт за {date} ещё не сдан.\n"
              "Нажмите «{btn}» 👇",
    },
    "digest": {
        "uz": "🌙 <b>Kunlik xulosa — {date}</b>\n\n"
              "✅ Hisobot topshirdi: <b>{done}</b> / {total}\n⏳ Topshirmadi: <b>{missing}</b>\n",
        "ru": "🌙 <b>Итоги дня — {date}</b>\n\n"
              "✅ Сдали отчёт: <b>{done}</b> / {total}\n⏳ Не сдали: <b>{missing}</b>\n",
    },
    "digest_hint": {
        "uz": "\n\n📥 Faylni «{excel}» yoki «{word}» orqali yuklab oling.",
        "ru": "\n\n📥 Скачайте файл через «{excel}» или «{word}».",
    },

    # ------------------------------------------------------------ yordam
    "help_employee": {
        "uz": "<b>ℹ️ Bot haqida</b>\n\n"
              "«{org}» hodimlari kundalik hisobotlarini shu bot orqali topshiradilar.\n\n"
              "<b>{new}</b> — hisobotni yozish yoki tahrirlash:\n"
              "  1️⃣ Bajarilgan ishlar\n  2️⃣ Muammo va takliflar\n  3️⃣ Ertangi rejalar\n\n"
              "<b>{my}</b> — oxirgi hisobotlaringiz.\n<b>{profile}</b> — shaxsiy ma'lumotlaringiz.\n"
              "<b>{lang}</b> — tilni o'zgartirish.\n\n"
              "Bir kunga bitta hisobot saqlanadi — qayta yuborsangiz, avvalgisi yangilanadi.\n\n"
              "Buyruqlar: /start /hisobot /help /cancel",
        "ru": "<b>ℹ️ О боте</b>\n\n"
              "Сотрудники «{org}» сдают ежедневные отчёты через этот бот.\n\n"
              "<b>{new}</b> — написать или изменить отчёт:\n"
              "  1️⃣ Выполненные работы\n  2️⃣ Проблемы и предложения\n  3️⃣ Планы на завтра\n\n"
              "<b>{my}</b> — ваши последние отчёты.\n<b>{profile}</b> — ваши данные.\n"
              "<b>{lang}</b> — сменить язык.\n\n"
              "За день хранится один отчёт — повторная отправка обновит предыдущий.\n\n"
              "Команды: /start /hisobot /help /cancel",
    },
    "help_admin": {
        "uz": "<b>ℹ️ Boshqaruv paneli</b>\n\n"
              "<b>{today}</b> — bugungi hisobotlar.\n<b>{missing}</b> — topshirmagan hodimlar.\n"
              "<b>{excel}</b> / <b>{word}</b> — tanlangan davr hisobotlarini fayl qilib olish.\n"
              "<b>{employees}</b> — hodimlar, faollashtirish/o'chirish.\n"
              "<b>{stats}</b> — joriy oy ko'rsatkichlari.\n<b>{lang}</b> — tilni o'zgartirish.\n\n"
              "Hodim botga /start bosib, tabel raqamini kiritsa — F.I.Sh. va lavozimi "
              "avtomatik biriktiriladi va sizga xabar keladi.\n\n"
              "Buyruqlar: /start /excel /word /hodimlar /help",
        "ru": "<b>ℹ️ Панель руководителя</b>\n\n"
              "<b>{today}</b> — отчёты за сегодня.\n<b>{missing}</b> — кто не сдал.\n"
              "<b>{excel}</b> / <b>{word}</b> — выгрузка отчётов за период в файл.\n"
              "<b>{employees}</b> — сотрудники, включение/удаление.\n"
              "<b>{stats}</b> — показатели за текущий месяц.\n<b>{lang}</b> — сменить язык.\n\n"
              "Сотрудник нажимает /start, вводит табельный номер — Ф.И.О. и должность "
              "подставляются автоматически, а вам приходит уведомление.\n\n"
              "Команды: /start /excel /word /hodimlar /help",
    },

    # ------------------------------------------------------------ hujjatlar (Excel / Word)
    "doc_title": {
        "uz": "HODIMLARNING KUNDALIK HISOBOTLARI",
        "ru": "ЕЖЕДНЕВНЫЕ ОТЧЁТЫ СОТРУДНИКОВ",
    },
    "doc_subtitle": {"uz": "Kundalik hisobotlar", "ru": "Ежедневные отчёты"},
    "doc_period": {"uz": "Davr", "ru": "Период"},
    "doc_generated": {"uz": "Hujjat shakllantirildi", "ru": "Документ сформирован"},
    "doc_total": {"uz": "Jami hisobotlar", "ru": "Всего отчётов"},
    "doc_empty": {
        "uz": "Tanlangan davr uchun hisobotlar topilmadi.",
        "ru": "За выбранный период отчётов не найдено.",
    },
    "doc_reports_count": {"uz": "{count} ta hisobot", "ru": "отчётов: {count}"},
    "doc_sign": {
        "uz": "Boshqarma boshlig'i    ______________________    {name}",
        "ru": "Начальник управления    ______________________    {name}",
    },
    "doc_sign_note": {
        "uz": "                                                    (imzo)",
        "ru": "                                                  (подпись)",
    },
    "doc_sign_label": {"uz": "Boshqarma boshlig'i", "ru": "Начальник управления"},
    "doc_sign_hint": {"uz": "(imzo)", "ru": "(подпись)"},
    "col_num": {"uz": "№", "ru": "№"},
    "col_tabel": {"uz": "№ Tabel", "ru": "Таб. №"},
    "col_date": {"uz": "Sana", "ru": "Дата"},
    "col_name": {"uz": "F.I.Sh.", "ru": "Ф.И.О."},
    "col_position": {"uz": "Lavozimi", "ru": "Должность"},
    "col_name_position": {"uz": "F.I.Sh. / Lavozimi", "ru": "Ф.И.О. / должность"},
    "col_done": {"uz": "Bajarilgan ishlar", "ru": "Выполненные работы"},
    "col_problems": {"uz": "Muammo va takliflar", "ru": "Проблемы и предложения"},
    "col_plans": {"uz": "Ertangi rejalar", "ru": "Планы на завтра"},
    "col_sent_at": {"uz": "Yuborilgan vaqt", "ru": "Время отправки"},
    "sheet_reports": {"uz": "Hisobotlar", "ru": "Отчёты"},
    "sheet_summary": {"uz": "Umumiy ko'rsatkich", "ru": "Сводка"},
    "col_report_count": {"uz": "Hisobotlar soni", "ru": "Кол-во отчётов"},
    "col_last_report": {"uz": "Oxirgi hisobot", "ru": "Последний отчёт"},
    "total_row": {"uz": "JAMI", "ru": "ИТОГО"},
}


def t(lang: str | None, key: str, **kwargs) -> str:
    """Kalit bo'yicha matnni tanlangan tilda qaytaradi."""
    entry = TEXTS.get(key)
    if entry is None:
        return key
    text = entry.get(lang or DEFAULT_LANG) or entry[DEFAULT_LANG]
    return text.format(**kwargs) if kwargs else text


def all_variants(key: str) -> set[str]:
    """Kalitning barcha tillardagi matnlari (tugma filtrlari uchun)."""
    entry = TEXTS.get(key, {})
    return {value for value in entry.values() if value}


def matches(key: str, text: str | None) -> bool:
    return bool(text) and text in all_variants(key)
