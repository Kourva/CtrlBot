# Link command
# ─────────────────────────────────────────────────────────────
def link_command(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:

    # Initialize variables
    chatid: str = message.chat.id

    # Try to generate link for user
    try:
        # Making reply markup for link options
        Markups: ClassVar[Any] = telebot.util.quick_markup({
            "Basic Invite": {
                "callback_data": f"Link@Basic"
            },
            "Solo Invite": {
                "callback_data": f"Link@Solo"
            },
            "Approval Invite": {
                "callback_data": f"Link@Approval"
            }

        }, row_width=2)

        # Get group's details
        chat_info: ClassVar[Any] = bot.get_chat(chatid)
        text: str = (
            f"{chat_info.title}\n"
            f"{chat_info.description}\n"
        )

        # Send link to user
        if message.reply_to_message:
            bot.send_message(
                chat_id=chatid,
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