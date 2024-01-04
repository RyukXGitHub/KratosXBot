import html
import json
import re
from time import sleep

import requests
from telegram import (
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
    User,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    run_async,
)
from telegram.utils.helpers import mention_html

import KratosXBot.modules.sql.chatbot_sql as sql
from KratosXBot import BOT_ID, BOT_NAME, BOT_USERNAME, dispatcher
from KratosXBot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from KratosXBot.modules.log_channel import gloggable


@run_async
@user_admin_no_reply
@gloggable
def kratosrm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_kratos = sql.set_kratos(chat.id)
        if is_kratos:
            is_kratos = sql.set_kratos(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI_DISABLED\n"
                f"<b>Admin :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "{} Chatbot Disabled by {}.".format(
                    dispatcher.bot.first_name, mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )

    return ""


@run_async
@user_admin_no_reply
@gloggable
def kratosadd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_kratos = sql.rem_kratos(chat.id)
        if is_kratos:
            is_kratos = sql.rem_kratos(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI_ENABLE\n"
                f"<b>Admin :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "{} Chatbot Enabled by {}.".format(
                    dispatcher.bot.first_name, mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )

    return ""


@run_async
@user_admin
@gloggable
def kratos(update: Update, context: CallbackContext):
    message = update.effective_message
    msg = "• Choose an option to enable/disable chatbot."
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Enable", callback_data="add_chat({})"),
                InlineKeyboardButton(text="Disable", callback_data="rm_chat({})"),
            ],
        ]
    )
    message.reply_text(
        text=msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


def kratos_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "kratos":
        return True
    elif BOT_USERNAME in message.text.upper():
        return True
    elif reply_message:
        if reply_message.from_user.id == BOT_ID:
            return True
    else:
        return False


def chatbot(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot
    is_kratos = sql.is_kratos(chat_id)
    if is_kratos:
        return

    if message.text and not message.document:
        if not kratos_message(context, message):
            return
        bot.send_chat_action(chat_id, action="typing")
        
        # Updated payload with 'model' and 'messages'
        payload = {
            "model": "pplx-70b-chat",  # Replace with your actual model name
            "messages": [{"role": "user", "content": message.text}]
        }
        
        # Your API endpoint and key
        api_url = "https://api.perplexity.ai/chat/completions"
        api_key = "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"  # Replace with your actual API key
        
        # Preparing the data to send
        payload = {
            "prompt": message.text,
            "max_tokens": 150  # Adjust as per your preference
        }
        
        # Headers for the POST request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Making the POST request to your API
        response = requests.post(api_url, json=payload, headers=headers)
        
        # Assuming the response contains a JSON with the key 'text' for the reply
        if response.status_code == 200:
            results = response.json()
            reply_text = results.get("text", "Sorry, I couldn't process that.")
        else:
            reply_text = f"Error: {response.status_code}, {response.text}"

        message.reply_text(reply_text)





__help__ = f"""
*{BOT_NAME} has an chatbot which provides you a seemingless chatting experience :*

 »  /chatbot *:* Shows chatbot control panel
"""

__mod_name__ = "ChatBot"


CHATBOTK_HANDLER = CommandHandler("chatbot", kratos)
ADD_CHAT_HANDLER = CallbackQueryHandler(kratosadd, pattern=r"add_chat")
RM_CHAT_HANDLER = CallbackQueryHandler(kratosrm, pattern=r"rm_chat")
CHATBOT_HANDLER = MessageHandler(
    Filters.text
    & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!") & ~Filters.regex(r"^\/")),
    chatbot,
)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    CHATBOT_HANDLER,
]
