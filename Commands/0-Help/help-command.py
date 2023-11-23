# Help command handler
# ─────────────────────────────────────────────────────────────
def help(bot: ClassVar[Any], message= ClassVar[Any]) -> NoReturn:
    try:
        # Create user object
        user: ClassVar[str, int] = User(message.reply_to_message or message)

        # Making reply markup for help
        Markups: ClassVar[Any] = telebot.util.quick_markup({
            "Website": {
                "url": "https://kourva.github.io/GroupCtrl"
            },
            "Channel": {
                "url": "https://t.me/GroupCtrl"
            },
            "Get on Private chat": {
                "callback_data": f"Send_Help_Private@{user.id}"
            }
        }, row_width=2)

        # Send message to user
        text: str = (
            f"Hi {user.fn or user.ln or user.un or user.id}\n"
            f"Choose your method to get help!"
        )
        if message.reply_to_message:
            bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_to_message_id=message.reply_to_message.message_id,
                reply_markup=Markups
            )
        else:
            bot.reply_to(
                message=message,
                text=text,
                reply_markup=Markups
            )

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}",
        )