# Handle service content types
# ─────────────────────────────────────────────────────────────
@bot.message_handler(content_types=telebot.util.content_type_service)
def handle_service_message(message: ClassVar[Any]) -> NoReturn:
    # Get chat info
    chat : str = message.chat.id
    path: str = f"Accounts/{chat}/members.json"
    
    # Handle member left 
    if message.content_type == "left_chat_member":
        # Get user id which left the group
        user_id: int = message.left_chat_member.id

        # get group members
        try:
            with open(path, "r") as file:
                members: Dict[str, Any] = json.load(file)
        except:
            return

        if str(user_id) in members.keys():
            del members[str(user_id)]

        # Update members database
        with open(path, "w") as file:
            json.dump(members, file, indent=4)


    # Handle member join
    elif message.content_type == "new_chat_members":
        # Get user id which join the group
        user: ClassVar[str, int] = message.new_chat_members[0]

        # get group members
        try:
            with open(path, "r") as file:
                members: Dict[str, Any] = json.load(file)
        except:
            return

        if str(user.id) not in members.keys():
            members[str(user.id)] = {
                "Firstname": user.first_name,
                "Lastname": user.last_name,
                "Username": user.username,
                "messageCount": 0
            }

        # Update members database
        with open(path, "w") as file:
            json.dump(members, file, indent=4)

    # Delete service message
    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )