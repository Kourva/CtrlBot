# Pin function to pin message in group
# ─────────────────────────────────────────────────────────────
def pin(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:
    # Initialize variables
    chat: str = message.chat.id
    try:
        bot.pin_chat_message(
            chat_id=chat,
            message_id=message.reply_to_message.message_id
        )
        bot.reply_to(
            message=message, 
            text=get_title(chat, "PinMessage")
        )

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}"
        )   


# unPin function to unpin message in group
# ─────────────────────────────────────────────────────────────
def unpin(bot: ClassVar[Any], 
          message: ClassVar[Any], 
          all_pins: Optional[bool] = False) -> NoReturn:
    # Initialize variables
    chat: str = message.chat.id

    try:
        # Unpin all messages
        if all_pins:
            bot.unpin_all_chat_messages(
                chat_id=chat,
            )
            bot.reply_to(
                message=message, 
                text=get_title(chat, "UnpinAllMessage")
            )
        
        # Unpin single message
        else:
            bot.unpin_chat_message(
                chat_id=chat,
                message_id=message.reply_to_message.message_id
            )
            bot.reply_to(
                message=message, 
                text=get_title(chat, "UnpinMessage")
            )

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}"
        ) 