# Mute function
# ─────────────────────────────────────────────────────────────
def mute(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:
    try:
        # Initialize variables
        chat: str = message.chat.id
        user: ClassVar[str, int] = User(message.reply_to_message)
        
        input_time: int
        try:
            input_time = int(message.text.split()[1].strip())
        except IndexError:
            input_time = 1
        except ValueError:
            return

        # If the user is not muted, mute user for specific minutes
        if bot.get_chat_member(chat, user.id).can_send_messages:
            bot.restrict_chat_member(
                chat_id=chat,
                user_id=user.id,
                until_date=int(time.time()) + (input_time * 60),
                permissions=telebot.types.ChatPermissions(
                    can_send_messages=False, 
                    can_send_media_messages=False, 
                    can_send_polls=False, 
                    can_send_other_messages=False, 
                    can_add_web_page_previews=False, 
                    can_change_info=False, 
                    can_invite_users=False, 
                    can_pin_messages=False
                )
            )
            bot.reply_to(
                message=message,
                text=get_title(chat, "MuteUser").format(
                    f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}](tg://user?id={user.id})",
                    input_time,
                ),
                parse_mode="MarkdownV2"
            )

        # Do nothing if user is already muted
        else:
            bot.reply_to(
                message=message,
                text=get_title(chat, "MuteAlready").format(
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


# UnMute function
# ─────────────────────────────────────────────────────────────
def unmute(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:
    try:
        # Initialize path for warn file
        chat: str = message.chat.id
        path: str = f"Accounts/{chat}/warned.json"
        user: ClassVar[str, int] = User(message.reply_to_message)

        # If user is muted, unMute user
        if not bot.get_chat_member(chat, user.id).can_send_messages:
            bot.restrict_chat_member(
                chat_id=chat,
                user_id=user.id,
                until_date=int(time.time()),
                permissions=telebot.types.ChatPermissions(
                    can_send_messages=True, 
                    can_send_media_messages=True, 
                    can_send_polls=True, 
                    can_send_other_messages=True, 
                    can_add_web_page_previews=False, 
                    can_change_info=False, 
                    can_invite_users=True, 
                    can_pin_messages=False
                )
            )
            bot.reply_to(
                message=message,
                text=get_title(chat, "UnmuteUser").format(
                    f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}](tg://user?id={user.id})",
                ),
                parse_mode="MarkdownV2"
            )

            # Load warned users from the JSON file if it exists
            try:
                with open(path, "r") as file:
                    warns: Dicty[str, Any] = json.load(file)

            # If the file doesn't exist, initialize an empty dict
            except FileNotFoundError:
                warns: Dicty[str, Any] = {}

            # If the user is not in the dict, add them
            if str(user.id) in warns.keys():
                warns[str(user.id)]["warnCount"] = 0

            # Reload warned list
            with open(path, 'w') as file:
                json.dump(warns, file, indent=4)

        # Do nothing if user is already unMuted or can send message
        else:
            bot.reply_to(
                message=message,
                text=get_title(chat, "UnmuteAlready").format(
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