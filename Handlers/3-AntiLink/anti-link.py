# Anti-Link handler using regular expression
# ─────────────────────────────────────────────────────────────
@bot.message_handler(regexp=setting.LINK_REGIX)
def handle_message_with_url(message: ClassVar[Any]) -> NoReturn:
    try:
        # Initialize Group's Chat-ID
        chat: str = message.chat.id

        # Get user data
        user: ClassVar[str, int] = setting.User(message)
        data: ClassVar[Any] = bot.get_chat_member(chat, user.id)

        # Check user privilege
        if not setting.is_co_admin(chat, user.id) \
            and not setting.privilege_checker(data):
            # Respond to messages containing URLs
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id
            )

    except Exception as error:
        bot.reply_to(
            message=message,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}"
        )