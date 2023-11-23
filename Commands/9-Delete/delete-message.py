# Delete command
# ─────────────────────────────────────────────────────────────
def del_message(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:

    # Initialize variables
    chatid: str = message.chat.id
    target: int = message.reply_to_message.message_id

    # Try to delete message
    try:
        bot.delete_message(
            chat_id=chatid,
            message_id=target
        )
        bot.delete_message(
            chat_id=chatid,
            message_id=message.message_id
        )

    # Send error log to support admin
    except Exception as error:
        bot.reply_to(
            message=message, 
            title=get_title(chatid, "DeleteMessageFail")
        )
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}",
        )