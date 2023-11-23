# Helper function to load group data
# ─────────────────────────────────────────────────────────────
def load_json_file(file_path: str) -> Dict[int,Any]:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Stat function
# ─────────────────────────────────────────────────────────────
def stat(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:
    try:
        # Get chat ID and user information from the message.
        chat: str = message.chat.id
        user: ClassVar[Union[str, int]] = User(message)

        # Send a waiting prompt to the user.
        prompt: ClassVar[Any] = bot.reply_to(
            message=message, 
            text=get_title(chat, "StatWait"), 
            parse_mode="MarkdownV2"
        )

        # Initialize the output list with the history statistic.
        history: Dict[int] = load_json_file(f"Accounts/{chat}/history.json")
        Output: List[str] = [
            get_title(chat, "HistoryStat").format(
                history.get('text', 0),
                history.get('audio', 0),
                history.get('document', 0),
                history.get('animation', 0),
                history.get('photo', 0),
                history.get('sticker', 0),
                history.get('video', 0),
                history.get('video_note', 0),
                history.get('voice', 0)
            )
        ]

        # Load member data from a JSON file and sort it by message count.
        members: Dict[Dict[str, int]] = load_json_file(f"Accounts/{chat}/members.json")
        sorted_members: Dict[Dict[str, int]] = sorted(
            members.items(), 
            key=lambda x: x[1].get("messageCount", 0), reverse=True
        )

        # Iterate through the top 30 members and format their statistics.
        for idx, (mid, member_data) in enumerate(sorted_members[:5], start=1):
            # Extract member's info
            username: str = member_data.get('Username', '')
            firstname: str = member_data.get('Firstname', '')
            message_count: int = member_data.get('messageCount', 0)
            name: str = firstname or username

            # Get member's stat title
            member_stat: str = get_title(chat, "MemberStat").format(
                idx, 
                f"[{escape_markdown_v2(name)}]"
                f"(tg://user?id={mid})", message_count
            )

            # Append result to output variable
            Output.append(member_stat)

        # Edit the waiting prompt with the final statistics.
        bot.edit_message_text(
            chat_id=chat, 
            message_id=prompt.message_id, 
            text="".join(Output), 
            parse_mode="MarkdownV2"
        )

    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}"
        ) 