#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ╭───────────────────────────────────────────────────────────╮
# │                       CTRL Guard Bot                      │
# │        << Powerful Group Guard bot for Telegram >>        │
# ╰┬──────────────────────────────────────────────────────────╯
#  ┴ Author : Kourva       https://github.com/Kourva         ◈
#  │ Source : CtrlBot      https://github.com/Kourva/CtrlBot ┬
#  ┬ Website: CtrlBot      https://Kourva.github.io/CtrlBot  │
#  │ Group  : GroupCtrl    https://t.me/GroupCtrl            │
#  ╰─────────────────────────────────────────────────────────╯

# Standard library modules
# ─────────────────────────────────────────────────────────────
import re
import os
import time
import json
from urllib.parse import quote
from typing import (
    ClassVar, 
    Optional, 
    Callable, 
    NoReturn, 
    Union,
    Any,
    List,
    Tuple,
    Dict
)

# Third-party modules
# ─────────────────────────────────────────────────────────────
import telebot

# Custom modules
# ─────────────────────────────────────────────────────────────
import setting
import commands
from titles import get_title

# Initialize bot token
# ─────────────────────────────────────────────────────────────
token: str = setting.TOKEN
if setting.token_checker(token):
    bot: ClassVar[Any] = telebot.TeleBot(token)
else:
    exit("[*] Token is invalid! Please use valid token.")


# Execute handlers
# ─────────────────────────────────────────────────────────────
# Iterate through files in the directory
for root, dirs, files in os.walk("Handlers"):
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


# Start command handler
# ─────────────────────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def start_command_handler(message: ClassVar[Any]) -> NoReturn:
    # Get user details
    user: ClassVar[str, int] = setting.User(message)

    # Initialize share link & text
    share_link: str = setting.SHARE_TEXT
    share_text: str = setting.SHARE_LINK

    # set reply markup to add bot to group
    markup: ClassVar[Any] = telebot.util.quick_markup({
        "Add To Group": {
            "url": f"tg://resolve?domain={bot.get_me().username}&startgroup"
        },
        "Share The Bot": {
            "url": f"tg://msg_url?url={quote(share_link)}&text={quote(share_text)}"
        }
    }, row_width=2)

    # Send message to user
    bot.reply_to(
        message=message,
        text=(
            f"Hello {user.fn}\n\nAdd me to your group "
            f"and give me admin privilege to start!"
        ),
        reply_markup=markup
    )


# Handle group and supergroup messages
# ─────────────────────────────────────────────────────────────
@bot.message_handler(
    func=lambda message: message.chat.type in ['group', 'supergroup'], 
    content_types=telebot.util.content_type_media
)
def group_chat_handler(message: ClassVar[Any]) -> NoReturn:

    # Initialize Group's Chat-ID & Group's Data
    chat: str = message.chat.id
    setting.initialize_chat(chat)
    user: ClassVar[str, int] = setting.User(message)

    # Check content lock status
    if setting.lock_check(bot, message):
        bot.delete_message(
            chat_id=message.chat.id, 
            message_id=message.message_id
        )
        bot.send_message(
            chat_id=chat,
            text=get_title(chat, "LockAlert").format(
                f"[{setting.escape_markdown_v2(user.fn or user.ln or user.un or user.id)}](tg://user?id={user.id})",
                "forwarded message" if message.forward_from else message.content_type
            ),
            parse_mode="MarkdownV2"
        )
        return

    # Process Group's history and Member status
    setting.processor(bot, message)

    # Get requester data
    user1: ClassVar[str, int] = setting.User(message)
    data1: ClassVar[Any] = bot.get_chat_member(chat, user1.id)

    # Handle text commands
    if message.content_type == "text":
        # User input
        user_input: str = message.text.strip().lower()

        # Admin required commands
        if (setting.privilege_checker(data1)
            or user1.id == setting.SUPPORT
                or setting.is_co_admin(chat, user.id)
            ):
            # Information and Help Commands
            # ─────────────────────────────────────────────────────────────
            # Help command
            if user_input in commands.help:
                setting.help(bot, message)

            # Info command
            elif user_input in commands.info:
                if message.reply_to_message:
                    setting.info(bot, message, reply=True)
                else:
                    setting.info(bot, message, reply=False)

            # Bot command
            elif user_input in commands.bot:
                bot.reply_to(message, get_title(message.chat.id, "Ping"))

            # Moderation Commands
            # ─────────────────────────────────────────────────────────────
            # Warn command
            elif user_input in commands.warn:
                if message.reply_to_message:
                    # Get replied user data
                    user2: ClassVar[str, int] = setting.User(message.reply_to_message)
                    data2: ClassVar[Any] = bot.get_chat_member(chat, user2.id)
                    if not setting.privilege_checker(data2):
                        setting.warn(bot, message)
                    else:
                        setting.privilege_error(bot, message)
            
            # unWarn command
            elif user_input in commands.unwarn:
                if message.reply_to_message:
                    # Get replied user data
                    user2: ClassVar[str, int] = setting.User(message.reply_to_message)
                    data2: ClassVar[Any] = bot.get_chat_member(chat, user2.id)
                    if not setting.privilege_checker(data2):
                        setting.unwarn(bot, message)
                    else:
                        setting.privilege_error(bot, message)

            # Mute command
            elif user_input.startswith(tuple(commands.mute)):
                if message.reply_to_message:
                    # Get replied user data
                    user2: ClassVar[str, int] = setting.User(message.reply_to_message)
                    data2: ClassVar[Any] = bot.get_chat_member(chat, user2.id)
                    if not setting.privilege_checker(data2):
                        setting.mute(bot, message)
                    else:
                        setting.privilege_error(bot, message)

            # unMute command
            elif user_input in commands.unmute:
                if message.reply_to_message:
                    # Get replied user data
                    user2: ClassVar[str, int] = setting.User(message.reply_to_message)
                    data2: ClassVar[Any] = bot.get_chat_member(chat, user2.id)
                    if not setting.privilege_checker(data2):
                        setting.unmute(bot, message)
                    else:
                        setting.privilege_error(bot, message)

            # Ban command
            elif user_input.startswith(tuple(commands.ban)):
                if message.reply_to_message:
                    # Get replied user data
                    user2: ClassVar[str, int] = setting.User(message.reply_to_message)
                    data2: ClassVar[Any] = bot.get_chat_member(chat, user2.id)
                    if not setting.privilege_checker(data2):
                        setting.ban(bot, message, reply=True)
                    else:
                        setting.privilege_error(bot, message)
                else:
                    setting.ban(bot, message, reply=False)

            # unBan command
            elif user_input.startswith(tuple(commands.unban)):
                if message.reply_to_message:
                    # Get replied user data
                    user2: ClassVar[str, int] = setting.User(message.reply_to_message)
                    data2: ClassVar[Any] = bot.get_chat_member(chat, user2.id)
                    if not setting.privilege_checker(data2):
                        setting.unban(bot, message, reply=True)
                    else:
                        setting.privilege_error(bot, message)
                else:
                    setting.unban(bot, message, reply=False)

            # VIP & Admin Management Commands
            # ─────────────────────────────────────────────────────────────
            # AddVIP command
            elif user_input in commands.addvip:
                if message.reply_to_message:
                    setting.vip_handler(bot, message, add=True)
            
            # DelVIP command
            elif user_input in commands.delvip:
                if message.reply_to_message:
                    setting.vip_handler(bot, message, add=False)

            # Promote command
            elif user_input in commands.promote:
                if message.reply_to_message:
                    setting.co_admin_handler(bot, message, add=True)
            
            # Demote command
            elif user_input in commands.demote:
                if message.reply_to_message:
                    setting.co_admin_handler(bot, message, add=False)

            # Pin and Unpin Commands
            # ─────────────────────────────────────────────────────────────     
            # Pin command
            elif user_input in commands.pin:
                if message.reply_to_message:
                    setting.pin(bot, message)
            
            # unPin commands
            elif user_input in commands.unpin:
                if message.reply_to_message:
                    setting.unpin(bot, message, all_pins=False)
                else:
                    setting.unpin(bot, message, all_pins=True)

            # Statistics and Bot-related Commands
            # ─────────────────────────────────────────────────────────────
            # Stats command
            elif user_input in commands.stats:
                setting.stat(bot, message)

            # Mention command
            elif user_input in commands.mention:
                setting.mention(bot, message)

            # Delete command
            elif user_input in commands.delete:
                if message.reply_to_message:
                    setting.del_message(bot, message)

            # Language command
            elif user_input in commands.language:
                setting.language(bot, message)

            # Link command
            elif user_input in commands.link:
                setting.link_command(bot, message)

            # Media type LOCK / UNLOCK Commands
            # ─────────────────────────────────────────────────────────────
            elif user_input in setting.LOCK_MAPPING:
                # Get content type
                content_type: str = setting.LOCK_MAPPING[user_input]
        
                # Lock/Unlock content
                if user_input.startswith("unlock"):
                    setting.unlock_content(bot, message, content_type)
                else:
                    setting.lock_content(bot, message, content_type)


# Start infinite polling mode
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)
