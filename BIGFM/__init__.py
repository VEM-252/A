import asyncio
import uvloop

# --- Loop Fix Start ---
# Ye hissa uvloop ko set karega taaki 'No Event Loop' error na aaye
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
# --- Loop Fix End ---

from BIGFM.core.bot import Aviax
from BIGFM.core.dir import dirr
from BIGFM.core.git import git
from BIGFM.core.userbot import Userbot
from BIGFM.misc import dbb, heroku

from .logging import LOGGER

# Zaroori functions call karein
dirr()
git()
dbb()
heroku()

app = Aviax()
userbot = Userbot()

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
