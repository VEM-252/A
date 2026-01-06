import time
from pyrogram import filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from youtubesearchpython.__future__ import VideosSearch

import config
from BIGFM import app
from BIGFM.misc import _boot_
from BIGFM.plugins.sudo.sudoers import sudoers_list
from BIGFM.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from BIGFM.utils import bot_sys_stats
from BIGFM.utils.decorators.language import LanguageStart
from BIGFM.utils.formatters import get_readable_time
from BIGFM.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# --- [ FIX: ABOUT TEXT FUNCTION WITH HTML FOR CLEAN LINKS ] ---
def get_about_text():
    DEV_USERNAME = "KIRU_OP" # Apna Username yahan likhein
    CH_LINK = config.SUPPORT_CHANNEL # Config se channel link
    
    return f"""
🎧 <b>sʜʏᴧᴍ ᴠɪʙє [ 🇮🇳 | 🌸 ]</b> ɪs ᴀ ᴘᴏᴡᴇʀғᴜʟ ᴀɴᴅ ʜɪɢʜ-ᴘᴇʀғᴏʀᴍᴀɴᴄᴇ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ʙᴏᴛ ᴅᴇsɪɢɴᴇᴅ ᴛᴏ ᴅᴇʟɪᴠᴇʀ ᴄʀʏsᴛᴀʟ-ᴄᴇᴀʀ ᴀᴜᴅɪᴏ sᴛʀᴇᴀᴍɪɴɢ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ᴡɪᴛʜ ᴇᴀsᴇ. ᴇɴᴊᴏʏ sᴍᴏᴏᴛʜ ᴘʟᴀʏʙᴀᴄᴋ, ᴀᴅᴠᴀɴᴄᴇᴅ ᴄᴏɴᴛʀᴏʟs ᴀɴᴅ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴍᴜsɪᴄ ᴇxᴘᴇʀɪᴇɴᴄᴇ ✨

❖ <b>ʙᴏᴛ ғᴜʟʟ ɪɴғᴏʀᴍᴀᴛɪᴏɴ :</b>
├──🚀 <b>ᴠᴇʀsɪᴏɴ</b> : <code>𝟷.𝟶.𝟶</code>
├──👨‍💻 <b>ᴅᴇᴠᴇʟᴏᴘᴇʀ</b> : @{DEV_USERNAME}
├──📢 <b>ᴜᴘᴅᴀᴛᴇ's</b> : <a href='{CH_LINK}'>ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ</a>
├──💾 <b>ᴅᴀᴛᴀʙᴀsᴇ</b> : <code>ᴍᴏɴɢᴏᴅʙ</code>
├──🖥️ <b>sᴇʀᴠᴇʀ</b> : <code>ᴠɪʀᴛᴜᴀʟ ᴘʀɪᴠᴀᴛᴇ sᴇʀᴠᴇʀ</code>
└──⚡ <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ</b> : <code>ʏᴏᴜᴛᴜʙᴇ ᴍᴜsɪᴄ</code>

📝 <b>ʟᴀɴɢᴜᴀɢᴇ & ғʀᴀᴍᴇᴡᴏʀᴋ :</b>
<i>ᴍᴏᴅᴇʀɴ ᴘʏᴛʜᴏɴ | ᴘʏ-ᴛɢᴄᴀʟʟs ᴠ𝟸.x | ᴘʏʀᴏɢʀᴀᴍ</i>

🟢 <b>ᴏɴʟɪɴᴇ sɪɴᴄᴇ :</b> <code>𝟶𝟷/𝟶𝟷/𝟸𝟶𝟸𝟻</code>

🔐 <b>ᴘʀɪᴠᴀᴄʏ ᴘᴏʟɪᴄʏ :</b>
<blockquote>ɪғ ʏᴏᴜ ᴜsᴇ <b>sʜʏᴧᴍ ᴠɪʙє [ 🇮🇳 | 🌸 ]</b> ғᴏʀ ᴀɴʏ ᴘᴜʀᴘᴏsᴇ, ʏᴏᴜ ᴀɢʀᴇᴇ ᴛᴏ ᴛʜᴇ ᴛᴇʀᴍs ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴs ᴡʀɪᴛᴛᴇɴ ɪɴ <code>/ᴘʀɪᴠᴀᴄʏ</code>. ᴛʜᴇ ᴘʀɪᴠᴀᴄʏ ᴘᴏʟɪᴄʏ ᴍᴀʏ ʙᴇ ᴜᴘᴅᴀᴛᴇᴅ ᴏʀ ᴄʜᴀɴɢᴇᴅ ᴀᴛ ᴀɴʏ ᴛɪᴍᴇ ᴡɪᴛʜᴏᴜᴛ ᴘʀɪᴏʀ ɴᴏᴛɪᴄᴇ.</blockquote>
"""

# --- [ FIX: ABOUT CALLBACK HANDLER ] ---
@app.on_callback_query(filters.regex("about_callback"))
async def on_about_click(client, query: CallbackQuery):
    await query.answer()
    await query.edit_message_text(
        text=get_about_text(),
        parse_mode=ParseMode.HTML, # HTML mode link chhupane ke liye zaroori hai
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("◁ ʙᴀᴄᴋ", callback_data="settingsback_helper")]]
        )
    )

# --- [ FIX: BACK BUTTON HANDLER ] ---
@app.on_callback_query(filters.regex("settingsback_helper"))
async def on_back_click(client, query: CallbackQuery):
    await query.answer()
    language = await get_lang(query.message.chat.id)
    _ = get_string(language)
    UP, CPU, RAM, DISK = await bot_sys_stats()
    out = private_panel(_)
    await query.edit_message_text(
        text=_["start_2"].format(query.from_user.mention, app.mention, UP, DISK, CPU, RAM),
        reply_markup=InlineKeyboardMarkup(out),
    )

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_GROUP),
                protect_content=True,
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text=_["S_B_8"], url=link),
                  InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_GROUP)]]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            return
    else:
        out = private_panel(_)
        UP, CPU, RAM, DISK = await bot_sys_stats()
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_2"].format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM),
            reply_markup=InlineKeyboardMarkup(out),
        )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

@app.on_message 
