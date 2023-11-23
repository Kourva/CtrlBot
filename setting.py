# Settings & Utilities for main source
# Standard library modules
# ─────────────────────────────────────────────────────────────
import os
import json
import re
import time
import sys
from typing import (
    ClassVar, 
    Optional, 
    Callable, 
    NoReturn, 
    Union,
    Any,
    List,
    Dict,
    Tuple
)

# Third-party modules
# ─────────────────────────────────────────────────────────────
import telebot

# Custom modules
# ─────────────────────────────────────────────────────────────
from titles import get_title

# Constant variables (Config variables)
# ─────────────────────────────────────────────────────────────
# Token for bot token
TOKEN: str = "Bot Token"

# Support or sponsor group ID
GROUP: str = "@Sponsor group username"

# Chat-ID of support admin to send errors 
SUPPORT: int = 1234567890

# Regular expression for Anti-Link
LINK_REGIX: str = r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?"

# Regular expression to validate bot TOKEN string
TOKEN_REGIX: str = r"[0-9]{9}:[a-zA-Z0-9_-]{35}\b"

# Share LINK & TEXT used to share bot
SHARE_TEXT: str = "t.me/BotUsername"
SHARE_LINK: str = (
    f"\n💥 Powerful & Free group guard bot for groups and super-groups!"
    f"\n\n👾 Start now and enjoy"
)

# All available commands
COMMANDS: List[str] = [
    "warn", "предупреждение", "اخطار",
    "unwarn", "удалить предупреждение", "حذف اخطار",
    "mute", "заглушить", "سکوت",
    "unmute", "снять заглушку", "حذف سکوت",
    "ban", "исключить", "بن",
    "unban", "добавитьдобавить", "حذف بن",
    "add vip", "добавить vip", "تنظیم ویژه",
    "del vip", "удалить vip", "حذف ویژه",
    "promote", "продвигать", "ترفیع",
    "demote", "понижать в должности", "تنزل",
    "info", "детали", "مشخصات",
    "pin", "прикрепить", "سنجاق",
    "unpin", "открепить", "حذف سنجاق",
    "delete", "убрать", "حذف",
    "language", "язык", "زبان",
    "stats", "статистика", "امار",
    "link", "ссылка", "لینک",
    "bot", "ping", "бот", "пинг", "ربات", "پینگ",
    "help", "usage", "помощь", "راهنما",
    "mention", "tag", "упомянуть", "تگ",
    "unpin all", "открепить все", "حذف کل سنجاق",
    "lock audio", "заблокировать аудио", "قفل صدا",
    "lock document", "заблокировать документ", "قفل فایل",
    "lock gif", "заблокировать гиф", "قفل گیف",
    "lock game", "заблокировать игру", "قفل بازی",
    "lock photo", "заблокировать фотографию", "قفل عکس",
    "lock sticker", "заблокировать стикер", "قفل استیکر",
    "lock video", "заблокировать видео", "قفل ویدیو",
    "lock video note", "заблокировать видео заметку", "قفل ویدیویی مسیج",
    "lock voice", "заблокировать голосовое сообщение", "قفل ویس",
    "lock contact", "заблокировать контакт", "قفل مخاطب",
    "lock location", "заблокировать местоположение", "قفل لوکیشن",
    "lock venue", "заблокировать место", "قفل مکان",
    "lock dice", "заблокировать кубик", "قفل تاس",
    "lock invoice", "заблокировать счёт", "قفل فاکتور",
    "lock successful payment", "заблокировать успешный платёж", "قفل پرداخت موفق",
    "lock connected website", "заблокировать подключенный веб сайт", "قفل وب سایت متصل",
    "lock poll", "заблокировать опрос", "قفل نظرسنجی",
    "lock passport data", "заблокировать паспортные данные", "قفل اطلاعات پاسپورت",
    "lock web app data", "заблокировать данные веб-приложения", "قفل داده های برنامه وب",
    "lock forward", "заблокировать вперед", "قفل فوروارد",
    "unlock audio", "разблокировать аудио", "بازکردن قفل صدا",
    "unlock document", "разблокировать документ", "بازکردن قفل فایل",
    "unlock gif", "разблокировать гиф", "بازکردن قفل گیف",
    "unlock game", "разблокировать игру", "بازکردن قفل بازی",
    "unlock photo", "разблокировать фотографию", "بازکردن قفل عکس",
    "unlock sticker", "разблокировать стикер", "بازکردن قفل استیکر",
    "unlock video", "разблокировать видео", "بازکردن قفل ویدیو",
    "unlock video note", "разблокировать видео заметку", "بازکردن قفل ویدیویی مسیج",
    "unlock voice", "разблокировать голосовое сообщение", "بازکردن قفل ویس",
    "unlock contact", "разблокировать контакт", "بازکردن قفل مخاطب",
    "unlock location", "разблокировать местоположение", "بازکردن قفل لوکیشن",
    "unlock venue", "разблокировать место", "بازکردن قفل مکان",
    "unlock dice", "разблокировать кубик", "بازکردن قفل تاس",
    "unlock invoice", "разблокировать счёт", "بازکردن قفل فاکتور",
    "unlock successful payment", "разблокировать успешный платёж", "بازکردن قفل پرداخت موفق",
    "unlock connected website", "разблокировать подключенный веб сайт", "بازکردن قفل وب سایت متصل",
    "unlock poll", "разблокировать опрос", "بازکردن قفل نظرسنجی",
    "unlock passport data", "разблокировать паспортные данные", "بازکردن قفل اطلاعات پاسپورت",
    "unlock web app data", "разблокировать данные веб-приложения", "بازکردن قفل داده های برنامه وب",
    "unlock forward", "разблокировать вперед", "باز کردن فوروارد"
]

# Lock command mapping
LOCK_MAPPING: Dict[str, Any] = {
    "lock audio": "audio",
    "lock document": "document",
    "lock gif": "animation",
    "lock game": "game",
    "lock photo": "photo",
    "lock sticker": "sticker",
    "lock video": "video",
    "lock video note": "video_note",
    "lock voice": "voice",
    "lock contact": "contact",
    "lock location": "location",
    "lock venue": "venue",
    "lock dice": "dice",
    "lock invoice": "invoice",
    "lock successful payment": "successful_payment",
    "lock connected website": "connected_website",
    "lock poll": "poll",
    "lock passport data": "passport_data",
    "lock web app data": "web_app_data",
    "lock forward": "forward",
    "unlock audio": "audio",
    "unlock document": "document",
    "unlock gif": "animation",
    "unlock game": "game",
    "unlock photo": "photo",
    "unlock sticker": "sticker",
    "unlock video": "video",
    "unlock video note": "video_note",
    "unlock voice": "voice",
    "unlock contact": "contact",
    "unlock location": "location",
    "unlock venue": "venue",
    "unlock dice": "dice",
    "unlock invoice": "invoice",
    "unlock successful payment": "successful_payment",
    "unlock connected website": "connected_website",
    "unlock poll": "poll",
    "unlock passport data": "passport_data",
    "unlock web app data": "web_app_data",
    "unlock forward": "forward"

}


# Custom User class for accessing easier to user info
# ─────────────────────────────────────────────────────────────
class User:
    def __init__(self, message: ClassVar[Any]) -> NoReturn:
        self.id: int = message.from_user.id          # chat-ID 
        self.fn: str = message.from_user.first_name  # First-name
        self.ln: str = message.from_user.last_name   # Last-name
        self.un: str = message.from_user.username    # Username


# Token validator
# ─────────────────────────────────────────────────────────────
def token_checker(token: str) -> bool:
    return bool(
        re.search(TOKEN_REGIX, token)
    )


# Privilege checker
# ─────────────────────────────────────────────────────────────
def privilege_checker(data: ClassVar[Any]) -> bool:
    return data.status in ["creator", "administrator"]


# Co-Admin checker (Bot admin)
# ─────────────────────────────────────────────────────────────
def is_co_admin(chat_id: str, user_id: int) -> bool:
    # Get co-admin lists
    with open(f"Accounts/{chat_id}/coadmins.json") as file:
        users: Dict[str, int] = json.load(file)

        # Return user's privilege
        return str(user_id) in users


# Privilege error message sender
# ─────────────────────────────────────────────────────────────
def privilege_error(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:
    # Send privilege error to user
    bot.reply_to(
        message=message,
        text=get_title(message.chat.id, "PrivilegeError")
    )


# Escape markdown V2 syntax
# ─────────────────────────────────────────────────────────────
def escape_markdown_v2(text: str) -> str:
    # Escape characters
    escape_chars: Dict[str, Any] = {
        '\\': '\\\\', '_': '\\_', '*': '\\*', '[': '\\[', ']': '\\]',
        '(': '\\(', ')': '\\)', '~': '\\~', '`': '\\`', '>': '\\>',
        '#': '\\#', '+': '\\+', '-': '\\-', '=': '\\=', '|': '\\|',
        '{': '\\{', '}': '\\}', '.': '\\.', '!': '\\!',
    }

    # Escapes the specified characters in the input text
    for char, escape_sequence in escape_chars.items():
        text = text.replace(char, escape_sequence)

    return text


# Initialize chat (Make config files for group data)
# ─────────────────────────────────────────────────────────────
def initialize_chat(chat: str) -> NoReturn:

    # Group path
    group: str = f"Accounts/{chat}"

    # If group is not registered, make new config
    if not os.path.exists(group):
        os.makedirs(group)

        # Create initial JSON files
        for file_name in [
            "warned.json",
            "history.json",
            "members.json",
            "vips.json",
            "coadmins.json"
        ]:
            with open(f"{group}/{file_name}", "w") as file:
                json.dump({}, file)

        # Create a language configuration file (default: "EN")
        with open(f"{group}/language", "w") as file:
            file.write("EN")

        # Create locks configuration file with default settings
        with open(f"{group}/locks.json", "w") as file:
            locks: Dict[bool] = {
                'audio': True, 'document': True, 'animation': False, 'game': True,
                'photo': True, 'sticker': False, 'video': True, 'video_note': True,
                'voice': True, 'contact': True, 'location': True, 'venue': True,
                'dice': False, 'invoice': True, 'successful_payment': True,
                'connected_website': True, 'poll': True, 'passport_data': True, 
                'web_app_data': True, 'forward': True
            }
            json.dump(locks, file, indent=4)


# Execute command handlers
# ─────────────────────────────────────────────────────────────
# Iterate through files in the directory
for root, dirs, files in os.walk("Commands"):
    # Exclude the "__pycache__" directory
    if "__pycache__" in dirs:
        dirs.remove("__pycache__")

    for file in files:
        # Check if the file has a ".py" extension
        if file.endswith(".py"):
            file_path: str = os.path.join(root, file)
            # Execute the Python file using exec
            with open(file_path, "r") as f:
                code: str = f.read()
                exec(code)
