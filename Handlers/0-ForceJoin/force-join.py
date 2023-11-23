# Force Join Handler (enforces users to join required channel)
# ─────────────────────────────────────────────────────────────

# Standard library modules
# ─────────────────────────────────────────────────────────────
from functools import wraps

# Force join decorator
# ─────────────────────────────────────────────────────────────
def requires_force_join(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(message: ClassVar[Any]) -> Callable:
        # Get data for user in group
        status = bot.get_chat_member(setting.GROUP, message.from_user.id).status

        # Check user subscription in channel
        if (status == "left"
            and message.content_type == "text" 
                and message.text.lower() in setting.COMMANDS):
            send_join_prompt(message)
            return

        # Return main function
        return func(message)

    # Helper function: Join prompt sender
    def send_join_prompt(message: ClassVar[Any]) -> NoReturn:
        # Set markup keyboard
        Markups = telebot.util.quick_markup(
            {
                "📢 Support Channel": {
                    "url": "t.me/{setting.GROUP[1:]}"
                }
            }
        )
        # Get users details
        user: ClassVar[str, int] = setting.User(message)

        # Send prompt to user
        bot.reply_to(
            message=message,
            text=(
                get_title(message.chat.id, "ForceJoin").format(
                    f"[{setting.escape_markdown_v2(user.fn or user.ln or user.un or user.id)}]"
                    f"(tg://user?id={message.from_user.id})"
                )
            ),
            reply_markup=Markups,
            parse_mode="MarkdownV2"
        )

    # Return wrapper
    return wrapper