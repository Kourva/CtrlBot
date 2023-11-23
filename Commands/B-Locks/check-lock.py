# Helper function to load group data
# ─────────────────────────────────────────────────────────────
def load_json_file(file_path: str) -> Dict:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Lock checker function
# ─────────────────────────────────────────────────────────────
def lock_check(bot: ClassVar[Any], message: ClassVar[Any]) -> bool:
    try:
        # Get chat ID from the message
        chat: str = message.chat.id
        user: int = message.from_user.id
        Type: str = message.content_type 
        status: Dict[str, bool] = load_json_file(f"Accounts/{chat}/locks.json")

        # Return false if user is admin
        if privilege_checker(bot.get_chat_member(chat_id=chat, user_id=user)):
            return False

        # Return false if user in co-admin (bot admin)
        if is_co_admin(chat, user):
            return False

        # Return false if user is VIP
        VIPs: Dict[str, Any] = load_json_file(f"Accounts/{chat}/vips.json")
        if str(user) in VIPs:
            return False

        # Check forward lock
        if message.forward_from:
            return status["forward"]

        # Return false if message is text
        if Type == "text":
            return False
        
        # Check lock status for group
        return status[Type]

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}"
        ) 