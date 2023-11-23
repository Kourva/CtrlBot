# Helper functiom to load vip members
# ─────────────────────────────────────────────────────────────
def get_vip_members(file_path: str) -> dict:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# VIP handler function
# ─────────────────────────────────────────────────────────────
def vip_handler(bot: ClassVar[Any], 
                message: ClassVar[Any], 
                add: Optional[bool] = True) -> NoReturn:
    try:
        # Initialize variables
        chat: str = message.chat.id
        user: ClassVar[str, int] = User(message.reply_to_message)
        path: str = f"Accounts/{chat}/vips.json"
        VIPs: Dict[str, Any] = get_vip_members(path)
        
        # Add user to VIP list
        if add:
            # Search for user that already exist
            if str(user.id) not in VIPs:
                VIPs[str(user.id)] = f"Added By admin {message.from_user.first_name}"

                # Update warns status for user
                with open(path, 'w') as file:
                    json.dump(VIPs, file, indent=4)

                # Send status messages
                bot.reply_to(
                    message=message,
                    text=get_title(chat, "VIPadded").format(
                        f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}]"
                        f"(tg://user?id={user.id})"
                    ),
                    parse_mode="MarkdownV2"
                    )
        
            else:
                bot.reply_to(
                    message=message,
                    text=get_title(chat, "VIPexist").format(
                        f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}]"
                        f"(tg://user?id={user.id})"
                    ),
                    parse_mode="MarkdownV2"
                )

        # Remove user from VIP list
        else:
            # Search for user that already exist
            if str(user.id) in VIPs:
                del VIPs[str(user.id)]

                # Update warns status for user
                with open(path, 'w') as file:
                    json.dump(VIPs, file, indent=4)

                # Send status messages
                bot.reply_to(
                    message=message,
                    text=get_title(chat, "VIPdeleted").format(
                        f"[{escape_markdown_v2(user.fn or user.ln or user.un or user.id)}](tg://user?id={user.id})"
                    ),
                    parse_mode="MarkdownV2"
                    )
        
            else:
                bot.reply_to(
                    message=message,
                    text=get_title(chat, "VIPnotexist").format(
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