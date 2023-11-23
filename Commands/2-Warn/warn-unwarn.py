# Get warns from group user
# ─────────────────────────────────────────────────────────────
def get_warns(chat_id: str) -> Dict[str, Any]:
    # Set path for group warned data
    path: str = f"Accounts/{chat_id}/warned.json"
    # Set default warn dict as empty
    warns: dict = {}

    # Try to fetch file content and continue as default if file not exist
    try:
        with open(path, "r") as file:
            warns: dict = json.load(file)
    except FileNotFoundError:
        pass
    
    # Return warns list
    return warns


# Update warn status
# ─────────────────────────────────────────────────────────────
def update_warns(chat_id: str, user: ClassVar[Any], warns: Dict) -> Union[Dict, NoReturn]:
    try:
        # Get user ID
        user_id_str: str = str(user.id)
    
        # Search for user in list
        if user_id_str not in warns:
            warns[user_id_str]: Dict[str, int] = {
                "Firstname": user.fn,
                "Lastname": user.ln,
                "Username": user.un,
                "warnCount": 0
            }

        # Add warn to user
        warns[user_id_str]["warnCount"] += 1
        # Return warns
        return warns

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}",
        )
        return False


# Handle the warn limitation
# ─────────────────────────────────────────────────────────────
def handle_warn_limit(bot: ClassVar[Any], chat_id: str, user: ClassVar[Any]) -> bool:
    try:
        # Mute the user for 24 hours
        bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            until_date=int(time.time()) + 86400,
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
        # Return true for success
        return True

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}",
        )
        return False


# Warn main function
# ─────────────────────────────────────────────────────────────
def warn(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:
    try:
        # Initialize variables
        chat: str = message.chat.id
        warns: Dict[str, int] = get_warns(chat)
        user: ClassVar[str, int] = User(message.reply_to_message)
        
        # Update warns status for user
        warns: Dict[str, int] = update_warns(chat, user, warns)
        with open(f"Accounts/{chat}/warned.json", 'w') as file:
            json.dump(warns, file, indent=4)

        # Handle warn limitation for maximum 5 warns
        if (wc:=warns[str(user.id)]["warnCount"]) < 5:
            bot.reply_to(
                message=message,
                text=get_title(chat, "WarnNormal").format(
                    f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}](tg://user?id={user.id})", wc
                ),
                parse_mode="MarkdownV2"
                )
        else:
            # Call warn limit handler if user reaches its limits
            if handle_warn_limit(bot, chat, user):
                bot.reply_to(
                    message=message,
                    text=get_title(chat, "WarnLimit").format(
                        f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}](tg://user?id={user.id})"
                    ),
                    parse_mode="MarkdownV2"
                )

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}",
        )


# unWarn main function 
# ─────────────────────────────────────────────────────────────
def unwarn(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:
    try:
        # Initialize variables
        chat: str = message.chat.id
        user: ClassVar[str, int] = User(message.reply_to_message)
        path: str = f"Accounts/{chat}/warned.json"
        user_id_str: str = str(user.id)
        warns: dict = get_warns(chat)

        # Check if the user is in the warns dictionary        
        if user_id_str in warns:
            # Decrease the user's warn count by 1
            warns[user_id_str]["warnCount"]: int = max(0, warns[user_id_str]["warnCount"] - 1)
            
            # Determine the reply text based on the updated warn count
            if warns[user_id_str]["warnCount"] > 0:
                reply_text: str = get_title(chat, "WarnDelete").format(
                    f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}](tg://user?id={user.id})",
                    warns[user_id_str]["warnCount"]
                )
            else:
                reply_text: str = get_title(chat, "WarnEmpty").format(
                    f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}](tg://user?id={user.id})"
                )
            
            # Reply to the message
            try:
                bot.reply_to(message=message, text=reply_text, parse_mode="MarkdownV2")
            except:
                pass
            
            # Save the updated warns back to the file
            with open(path, 'w') as file:
                json.dump(warns, file, indent=4)

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}",
        )
