# Language command handler
# Supported languages are [EN, RU, FA] and defaults to EN
# ─────────────────────────────────────────────────────────────
def language(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:
    try:
        # Get the chat ID and user information from the message.
        chat: str = message.chat.id
        user: ClassVar[Union[str, int]] = User(message)

        # Try to open a file to retrieve the language setting for the group.
        try:
            with open(f"Accounts/{chat}/language", "r") as file:
                lang: str = file.read().strip()
        # If the file is not found, set the language to English ("EN").
        except FileNotFoundError:
            lang: str = "EN"

        # Define keyboard markup with language options and a close button.
        Markups: ClassVar[Any] = telebot.util.quick_markup(
            {
                "🇺🇸 English": {
                    "callback_data": f"SetLang_EN_{chat}_{user.id}"
                },
                "🇷🇺 Русский": {
                    "callback_data": f"SetLang_RU_{chat}_{user.id}"
                },
                "🇮🇷 فارسی": {
                    "callback_data": f"SetLang_FA_{chat}_{user.id}"
                },
                "❌ Close": {
                    "callback_data": f"CloseLangMenu_{user.id}"
                },
            }, 
            row_width=2
        )

        # Send a message to the user with the language options.
        bot.reply_to(
            message=message,
            text=get_title(chat, "Language").format(lang),
            reply_markup=Markups,
        )

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}"
        )
