# Helper functiom to load co-admins
# ─────────────────────────────────────────────────────────────
def get_co_admins(file_path: str) -> Dict:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# VIP handler function
# ─────────────────────────────────────────────────────────────
def co_admin_handler(bot: ClassVar[Any], 
                     message: ClassVar[Any], 
                     add: Optional[bool] = True) -> NoReturn:
    try:
        # Initialize variables
        chat: str = message.chat.id
        user: ClassVar[str, int] = User(message.reply_to_message)
        path: str = f"Accounts/{chat}/coadmins.json"
        co_admins: Dict[str, Any] = get_co_admins(path)
        
        # Add user to VIP list
        if add:
            # Search for user that already exist
            if str(user.id) not in co_admins:
                co_admins[str(user.id)] = (
                    f"Added By admin {message.from_user.first_name}"
                )
                # Update warns status for user
                with open(path, 'w') as file:
                    json.dump(co_admins, file, indent=4)

                # Send status messages
                bot.reply_to(
                    message=message,
                    text=get_title(chat, "CoAadded").format(
                        f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}]"
                        f"(tg://user?id={user.id})"
                    ),
                    parse_mode="MarkdownV2"
                    )
        
            else:
                bot.reply_to(
                    message=message,
                    text=get_title(chat, "CoAexist").format(
                        f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}]"
                        f"(tg://user?id={user.id})"
                    ),
                    parse_mode="MarkdownV2"
                )

        # Remove user from VIP list
        else:
            # Search for user that already exist
            if str(user.id) in co_admins:
                del co_admins[str(user.id)]

                # Update warns status for user
                with open(path, 'w') as file:
                    json.dump(co_admins, file, indent=4)

                # Send status messages
                bot.reply_to(
                    message=message,
                    text=get_title(chat, "CoAdeleted").format(
                        f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}]"
                        f"(tg://user?id={user.id})"
                    ),
                    parse_mode="MarkdownV2"
                    )
        
            else:
                bot.reply_to(
                    message=message,
                    text=get_title(chat, "CoAnotexist").format(
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