# All available commands for bot in 3 languages
# Standard library modules
# ─────────────────────────────────────────────────────────────
from typing import List

# Information and Help Commands
# ─────────────────────────────────────────────────────────────
help: List[str] = ["help", "usage", "помощь", "راهنما"]
info: List[str] = ["info", "детали", "مشخصات"]
bot: List[str] = ["bot", "ping", "бот", "пинг", "ربات", "پینگ"]

# Moderation Commands
# ─────────────────────────────────────────────────────────────
warn: List[str] = ["warn", "предупреждение", "اخطار"]
unwarn: List[str] = ["unwarn", "удалить предупреждение", "حذف اخطار"]
mute: List[str] = ["mute", "заглушить", "سکوت"]
unmute: List[str] = ["unmute", "снять заглушку", "حذف سکوت"]
ban: List[str] = ["ban", "исключить", "بن"]
unban: List[str] = ["unban", "добавитьдобавить", "حذف بن"]

# VIP Management
# ─────────────────────────────────────────────────────────────
addvip: List[str] = ["add vip", "addvip", "добавить vip", "تنظیم ویژه"]
delvip: List[str] = ["del vip", "delvip", "удалить vip", "حذف ویژه"]
promote: List[str] = ["promote", "продвигать", "ترفیع"]
demote: List[str] = ["demote", "понижать в должности", "تنزل"]

# Pin and Unpin Commands
# ─────────────────────────────────────────────────────────────
pin: List[str] = ["pin", "прикрепить", "سنجاق"]
unpin: List[str] = ["unpin", "открепить", "حذف سنجاق"]

# Statistics and Bot-related Commands
# ─────────────────────────────────────────────────────────────
stats: List[str] = ["stats", "статистика", "امار"]
mention: List[str] = ["mention", "tag", "упомянуть", "تگ"]
delete: List[str] = ["delete", "убрать", "حذف"]
language: List[str] = ["language", "язык", "زبان"]
link: List[str] = ["link", "ссылка", "لینک"]