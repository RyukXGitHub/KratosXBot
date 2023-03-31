from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as telever
from telethon import __version__ as tlhver

from KratosXBot import BOT_NAME, BOT_USERNAME, OWNER_ID, START_IMG, SUPPORT_CHAT, pbot


@pbot.on_message(filters.command("alive"))
async def awake(_, message: Message):
    TEXT = f"**Hello {message.from_user.mention},\n\nI am {BOT_NAME}**\n━━━━━━━━━━━━━━━━━━━\n\n"
    TEXT += f"» **My Developer :** [RyukXGitHub](tg://user?id={OWNER_ID})\n\n"
    TEXT += f"» **Library Version :** `{telever}` \n\n"
    TEXT += f"» **Telethon Version :** `{tlhver}` \n\n"
    TEXT += f"» **Pyrogram Version :** `{pyrover}` \n━━━━━━━━━━━━━━━━━\n\n"
    BUTTON = [
        [
            InlineKeyboardButton("❓Help", url=f"https://t.me/{BOT_USERNAME}?start=help"),
            InlineKeyboardButton("🏥Support", url=f"https://t.me/{SUPPORT_CHAT}"),
        ]
    ]
    await message.reply_photo(
        photo=START_IMG,
        caption=TEXT,
        reply_markup=InlineKeyboardMarkup(BUTTON),
    )


__mod_name__ = "Alive
