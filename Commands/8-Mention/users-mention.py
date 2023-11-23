# Helper function to load a JSON file.
# ─────────────────────────────────────────────────────────────
def load_json_file(file_path: str) -> Dict:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Mention function to mention active users
# ─────────────────────────────────────────────────────────────
def mention(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:
    try:
        # Get chat ID and user information from the message.
        chat: str = message.chat.id
        user: ClassVar[str, int] = User(message)

        # Open members file
        members: dict = load_json_file(f"Accounts/{chat}/members.json")
        sorted_members: dict = sorted(members.items(), key=lambda x: x[1].get("messageCount", 0), reverse=True)

        # Initialize a list to store batches of mentions.
        mention_batches: list = []

        # Correct the member length to 50 if its bigger than 50
        length: int = min(len(sorted_members), 50)

        # Iterate through sorted members and create batches of 5 mentions.
        for idx in range(0, length, 10):
            mention_batch: dict = sorted_members[idx:idx+10]
            mention_strings: list = []

            # Create mention strings for this batch.
            for member_id, member_data in mention_batch:
                username: str = member_data.get('Username', '')
                firstname: str = member_data.get('Firstname', '')
                name: str = firstname or username or ormember_id
                mention_strings.append(f"✦ [{escape_markdown_v2(name)}](tg://user?id={member_id})")

            # Join the mention strings for this batch into one message.
            mention_message = " ".join(mention_strings)

            # Append this batch to the list of mention batches.
            mention_batches.append(mention_message)

        # Send each batch of mentions as a separate message.
        if (replied:=message.reply_to_message):
            for mention_message in mention_batches:
                bot.send_message(
                    chat_id=chat, 
                    text=mention_message, 
                    parse_mode="MarkdownV2",
                    reply_to_message_id=replied.message_id
                )
                time.sleep(1)

        else:
            for mention_message in mention_batches:
                bot.reply_to(
                    message=message, 
                    text=mention_message, 
                    parse_mode="MarkdownV2"
                )
                time.sleep(1)

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}",
        )