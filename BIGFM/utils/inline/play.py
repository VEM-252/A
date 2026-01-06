import math
from pyrogram.types import InlineKeyboardButton
from BIGFM.utils.formatters import time_to_seconds

# --- [ 1. PROGRESS BAR GENERATOR ] ---
def get_progress_bar(played_sec, total_sec):
    try:
        percentage = (played_sec / total_sec) * 100
    except ZeroDivisionError:
        percentage = 0
    
    umm = math.floor(percentage / 10) 

    if umm <= 0:
        bar = "◉—————————"
    elif umm == 1:
        bar = "—◉————————"
    elif umm == 2:
        bar = "——◉———————"
    elif umm == 3:
        bar = "———◉——————"
    elif umm == 4:
        bar = "————◉—————"
    elif umm == 5:
        bar = "—————◉————"
    elif umm == 6:
        bar = "——————◉———"
    elif umm == 7:
        bar = "———————◉——"
    elif umm == 8:
        bar = "————————◉—"
    elif umm >= 9:
        bar = "—————————◉"
    else:
        bar = "——————————"
    return bar

# --- [ 2. STREAM MARKUP TIMER ] ---
def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    progress_bar = get_progress_bar(played_sec, duration_sec)

    return [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="Ⅱ", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="⏭", callback_data=f"ADMIN Skip|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="↺", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text=f"{played} {progress_bar} {dur}", callback_data="timer_noop")
        ],
        [InlineKeyboardButton(text="𝐂𝐋𝐎𝐒𝐄", callback_data=f"ADMIN Stop|{chat_id}")],
    ]

# --- [ 3. SIMPLE STREAM MARKUP ] ---
def stream_markup(_, chat_id):
    return [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="Ⅱ", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="⏭", callback_data=f"ADMIN Skip|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="↺", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [InlineKeyboardButton(text="𝐂𝐋𝐎𝐒𝐄", callback_data=f"ADMIN Stop|{chat_id}")],
    ]

# --- [ 4. TRACK MARKUP ] ---
def track_markup(_, videoid, user_id, channel, fplay):
    return [
        [
            InlineKeyboardButton(text="ᴀᴜᴅɪᴏ", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text="ᴠɪᴅᴇᴏ", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"),
        ],
        [InlineKeyboardButton(text="𝐂𝐋𝐎𝐒𝐄", callback_data=f"forceclose {videoid}|{user_id}")],
    ]

# --- [ 5. MISSING: LIVESTREAM MARKUP ] ---
def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    return [
        [
            InlineKeyboardButton(text="ʟɪᴠᴇ sᴛʀᴇᴀᴍ", callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}"),
        ],
        [InlineKeyboardButton(text="𝐂𝐋𝐎𝐒𝐄", callback_data=f"forceclose {videoid}|{user_id}")],
    ]

# --- [ 6. MISSING: PLAYLIST MARKUP ] ---
def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    return [
        [
            InlineKeyboardButton(text="ᴀᴜᴅɪᴏ", callback_data=f"AviaxPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text="ᴠɪᴅᴇᴏ", callback_data=f"AviaxPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}"),
        ],
        [InlineKeyboardButton(text="𝐂𝐋𝐎𝐒𝐄", callback_data=f"forceclose {videoid}|{user_id}")],
    ]

# --- [ 7. SLIDER MARKUP ] ---
def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    return [
        [
            InlineKeyboardButton(text="ᴀᴜᴅɪᴏ", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text="ᴠɪᴅᴇᴏ", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"),
        ],
        [
            InlineKeyboardButton(text="◁", callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
            InlineKeyboardButton(text="𝐂𝐋𝐎𝐒𝐄", callback_data=f"forceclose {query}|{user_id}"),
            InlineKeyboardButton(text="▷", callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
        ],
    ]
