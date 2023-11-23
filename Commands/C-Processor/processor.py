# Add message history 
# ─────────────────────────────────────────────────────────────
def add_history(chat_dir: str, 
                user: ClassVar[Union[str, int]], 
                message: ClassVar[Any]) -> NoReturn:
    try:
        # Get history file path
        history_file: str = os.path.join(chat_dir, "history.json")

        # Get message type
        Type: str = message.content_type

        # Read story or defaults history to empty if file not found
        history: Dict[str, bool]
        try:
            with open(history_file, "r") as file:
                history = json.load(file)
        except FileNotFoundError:
            history = {}

        # Add user history to history data
        if Type in ['text', 'audio', 'document', 
                    'animation', 'photo', 'sticker', 
                    'video', 'video_note', 'voice'
                    ]:
            history[Type]: int = history.get(Type, 0) + 1

        # Save the history data
        with open(history_file, "w") as file:
            json.dump(history, file, indent=4)
    
    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}"
        )


# Update member status
# ─────────────────────────────────────────────────────────────
def update_member(chat_dir: str, user: ClassVar[Union[str, int]]) -> NoReturn:
    try:
        # Get file path
        members_file: str = os.path.join(chat_dir, "members.json")
        
        # Get members list or defaults it to empty list if file not found
        members: Dict[Dict[str, int]]
        try:
            with open(members_file, 'r') as file:
                members = json.load(file)
        except FileNotFoundError:
            members = {}

        # Add member if member no exist in members list
        if str(user.id) not in members:
            members[user.id]: Dict[int, str] = {
                "Firstname": user.fn,
                "Lastname": user.ln,
                "Username": user.un,
                "messageCount": 1
            }

        # Increase message count for member by 1
        else:
            members[str(user.id)]["messageCount"] += 1

        # Save members list to data
        with open(members_file, "w") as file:
            json.dump(members, file, indent=4)
            
    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}"
        )


# Process incoming messages from group
# ─────────────────────────────────────────────────────────────
def processor(bot: ClassVar[Any], message: ClassVar[Any]) -> NoReturn:
    try:
        # Initialize variables
        chat_dir: str = f"Accounts/{message.chat.id}"
        user: ClassVar[str, int] = User(message)

        # Add / Update member status and message to history
        update_member(chat_dir, user)
        add_history(chat_dir, user, message)
    
    # Send error log to support admin
    except Exception as error:
        bot.send_message(
            chat_id=SUPPORT,
            text=f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(error).__name__}"
        )
