# Callback handler
# ─────────────────────────────────────────────────────────────
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: ClassVar[Any]) -> NoReturn:
    # Set chat id
    chat: str = call.message.chat.id
    masg: str = call.message.message_id
    user: int = call.from_user.id

    # Handle close callback
    # ─────────────────────────────────────────────────────────────
    if call.data.startswith("CloseLangMenu"):
        requester: str = call.data.split("_")[1]
        # Validate requester
        if str(user) == requester:
            bot.edit_message_text(
                chat_id=chat,
                message_id=masg,
                text=get_title(chat, "CloseLangMenu")
            )
        else:
            bot.answer_callback_query(
                call.id,
                text=get_title(chat, "CallBackError"),
                show_alert=True
            )

    # Handle language action
    # ─────────────────────────────────────────────────────────────
    elif call.data.startswith("SetLang"):
        # Set language to be set, chatID and Requester iD
        lang: str
        chat: str
        requester: str
        _, lang, chat, requester = call.data.split("_")

        # Validate requester
        if str(user) == requester:
            # Change language for group
            path: str = f"Accounts/{chat}/language"
            with open(path, "r+") as file:
                prev: str = file.read().strip()
                file.seek(0)
                file.write(lang.strip().upper())

            # Send result to user
            bot.answer_callback_query(
                call.id,
                text=get_title(chat, "SetLangauge").format(lang, prev),
                show_alert=True
            )
            # CLose menu
            bot.edit_message_text(
                chat_id=chat,
                message_id=masg,
                text=get_title(chat, "CloseLangMenu")
            )

        else:
            bot.answer_callback_query(
                call.id,
                text=get_title(chat, "CallBackError"),
                show_alert=True
            )

    # Handle language action
    # ─────────────────────────────────────────────────────────────
    elif call.data.startswith("Send_Help_Private"):
        # Initialize variables
        user_id: str = call.data.split("@")[1].strip()
        try:
            # Validate requester
            if str(user_id) == str(user):
                # Send help message to user
                bot.answer_callback_query(
                    call.id,
                    text=get_title(chat, "PromptSent"),
                    show_alert=True
                )
                for message in ["7", "8", "9", "10", "11", "12"]:
                    bot.forward_message(
                        chat_id=user_id,
                        from_chat_id="@GroupCtrl",
                        message_id=message
                    )
                    time.sleep(1)
                # CLose menu
                bot.edit_message_text(
                    chat_id=chat,
                    message_id=masg,
                    text=get_title(chat, "CloseLangMenu")
                )
            else:
                bot.answer_callback_query(
                    call.id,
                    text=get_title(chat, "CallBackError"),
                    show_alert=True
                )
        
        except Exception as error:
            if "bot can't initiate conversation with a user" in str(error):
                bot.answer_callback_query(
                    call.id,
                    text=get_title(chat, "BotNotStarted"),
                    show_alert=True
                )
            elif "bot was blocked by the user" in str(error):
                bot.answer_callback_query(
                    call.id,
                    text=get_title(chat, "BotBlocked"),
                    show_alert=True
                )

    # Link generator
    # ─────────────────────────────────────────────────────────────
    elif call.data.startswith("Link@"):
        link_mode: str
        _, link_mode = call.data.split("@")
        if link_mode == "Basic":
            link: str = bot.create_chat_invite_link(
                chat_id=chat,
            ).invite_link

            # CLose menu
            bot.edit_message_text(
                chat_id=chat,
                message_id=masg,
                text=(
                    
                    f"{call.message.text}\n\n"
                    f"◂───────⌤(Basic)⌤───────▸\n"
                    f"{link}"
                ),
                disable_web_page_preview=True
            )

        elif link_mode == "Solo":
            link: str = bot.create_chat_invite_link(
                chat_id=chat,
                member_limit=1
            ).invite_link

            # CLose menu
            bot.edit_message_text(
                chat_id=chat,
                message_id=masg,
                text=(
                    f"{call.message.text}\n\n"
                    f"◂───────⌤(Solo)⌤───────▸\n"
                    f"{link}"
                ),
                disable_web_page_preview=True
            )

        elif link_mode == "Approval":
            link: str = bot.create_chat_invite_link(
                chat_id=chat,
                creates_join_request=True
            ).invite_link

            # CLose menu
            bot.edit_message_text(
                chat_id=chat,
                message_id=masg,
                text=(
                    f"{call.message.text}\n\n"
                    f"◂─────⌤(Approval)⌤─────▸\n"
                    f"{link}"
                ),
                disable_web_page_preview=True
            )
