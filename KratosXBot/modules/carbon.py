from pyrogram import filters

from KratosXBot import pbot
from KratosXBot.utils.errors import capture_err
from KratosXBot.utils.functions import make_carbon


@pbot.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a text to generate carbon.")
    if not message.reply_to_message.text:
        return await message.reply_text("Reply to a text to generate carbon.")
    m = await message.reply_text(`Generating Carbon...`)
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit(`Uploading Generated Carbon...`)
    await pbot.send_photo(message.chat.id, carbon)
    await m.delete()
    carbon.close()


__mod_name__ = "Carbon"

__help__ = """
Makes a carbon of the given text and send it to you.

❍ /carbon *:* Makes carbon if replied to a text.
 """
