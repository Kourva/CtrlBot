# BAN / UNBAN handler function
# ─────────────────────────────────────────────────────────────
def handle_reply(bot: ClassVar[Any],  message: ClassVar[Any],  ban: bool) -> NoReturn:
    try:
        # Initialize variables
        chat: str = message.chat.id
        user: ClassVar[Union[int, str]] = User(message.reply_to_message)

        # If user is not in group
        if ban and bot.get_chat_member(chat, user.id).status == "kicked":
            # Handle unbanning when user is not banned
            bot.reply_to(
                message=message,
                text=get_title(chat, "BanAlready").format(
                    f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}](tg://user?id={user.id})",
                ),
                parse_mode="MarkdownV2"
            )
            return

        # Ban or unBan member
        bot_method: Callable = bot.ban_chat_member if ban else bot.unban_chat_member
        bot_method(
            chat_id=chat,
            user_id=user.id
        )

        # Send action message
        action_name: str = "BanUser" if ban else "UnbanUser"
        bot.reply_to(
            message=message,
            text=get_title(chat, action_name).format(
                f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}]"
                f"(tg://user?id={user.id})"
            ),
            parse_mode="MarkdownV2"
        )

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}",
        )


# BAN / UNBAN function handler using argument
# ─────────────────────────────────────────────────────────────
def handle_args(bot: ClassVar[Any], message: ClassVar[Any], arg: str, ban: bool) -> NoReturn:
    # Initialize variables
    chat: str = message.chat.id
    user: str = arg

    try:
        # If user is not in group
        if ban and bot.get_chat_member(chat, arg).status == "kicked":
            # Handle unbanning when user is not banned
            bot.reply_to(
                message=message,
                text=get_title(chat, "BanAlready").format(
                    f"[ID {arg}](tg://user?id={arg})",
                ),
                parse_mode="MarkdownV2"
            )
            return

        # Ban or unBan member
        bot_method: Callable = bot.ban_chat_member if ban else bot.unban_chat_member
        bot_method(
            chat_id=chat,
            user_id=arg
        )

        # Send action message
        action_name: str = "BanUser" if ban else "UnbanUser"
        bot.reply_to(
            message=message,
            text=get_title(chat, action_name).format(
                f"[ID {arg}](tg://user?id={arg})",
            ),
            parse_mode="MarkdownV2"
        )

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}",
        )


# Main Ban function
# ─────────────────────────────────────────────────────────────
def ban(bot: ClassVar[Any], message: ClassVar[Any], reply=False) -> NoReturn:
    try:
        # Check for arguments
        if reply:
            handle_reply(bot=bot, message=message, ban=True)
        else:
            try:
                user = message.text.split()[1].strip()
                if user.isnumeric():
                    handle_args(bot=bot, message=message, arg=user, ban=True)
            except ValueError:
                return
            except IndexError:
                return
    
    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}",
        )    


# Main unBan function
# ─────────────────────────────────────────────────────────────
def unban(bot: ClassVar[Any], message: ClassVar[Any], reply=False) -> NoReturn:
    try:
        # Check for arguments
        if reply:
            handle_reply(bot=bot, message=message, ban=False)
        else:
            try:
                user = message.text.split()[1].strip()
                if user.isnumeric():
                    handle_args(bot=bot, message=message, arg=user, ban=False)
            except ValueError:
                return
            except IndexError:
                return
    
    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}",
        )    