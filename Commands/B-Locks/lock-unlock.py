# Helper function to get group data
# ─────────────────────────────────────────────────────────────
def load_json_file(file_path: str) -> Dict:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Lock function to lock content
# ─────────────────────────────────────────────────────────────
def lock_content(bot: ClassVar[Any], 
                 message: ClassVar[Any], 
                 content_type: str) -> NoReturn:
    # Get chat ID from the message.
    chat: str = message.chat.id
    path: str = f"Accounts/{chat}/locks.json"

    try:
        # Get lock status for group
        status: Dict[str, bool] = load_json_file(path)
        
        # If content type is already locked, send status message
        if status[content_type]:
            bot.reply_to(
                message=message,
                text=get_title(chat, f"LOCKEDALREADY{content_type}")
            )

        # Lock content and update json file
        else:
            status[content_type]: bool = True

            with open(path, "w") as file:
                json.dump(status, file, indent=4)

            bot.reply_to(
                message=message,
                text=get_title(chat, f"LOCK{content_type}")
            )

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}"
        )
        bot.reply_to(
            message=message,
            text=get_title(chat, f"LockFail")
        )


# Unlock function to unlock content
# ─────────────────────────────────────────────────────────────
def unlock_content(bot: ClassVar[Any], 
                   message: ClassVar[Any], 
                   content_type: str) -> NoReturn:
    # Get chat ID from the message.
    chat: str = message.chat.id
    path: str = f"Accounts/{chat}/locks.json"

    try:
        # Get lock status for group
        status: Dict[str, bool] = load_json_file(path)
        
        # UnLock content and update json file
        if status[content_type]:
            status[content_type]: bool = False

            with open(path, "w") as file:
                json.dump(status, file, indent=4)

            bot.reply_to(
                message=message,
                text=get_title(chat, f"UNLOCK{content_type}")
            )

        # If content is already unlocked send status message
        else:
            bot.reply_to(
                message=message,
                text=get_title(chat, f"UNLOCKEDALREADY{content_type}")
            )

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}"
        )
        bot.reply_to(
            message=message,
            text=get_title(chat, f"LockFail")
        )