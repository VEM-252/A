import asyncio
from typing import Union

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import (
    AudioPiped,
    AudioVideoPiped,
    HighQualityAudio,
    MediumQualityVideo,
    Update,
)
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.exceptions import (
    AlreadyJoined,
    NoActiveGroupCall,
    TelegramServerError,
)

import config
from BIGFM import LOGGER
from BIGFM.misc import db
from BIGFM.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    group_assistant,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
)
from BIGFM.utils.exceptions import AssistantErr
from BIGFM.utils.stream.autoclear import auto_clean
from strings import get_string


async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


class Call:
    def __init__(self):
        self.clients = []

        for i, string in enumerate(
            [config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5],
            start=1,
        ):
            if string and str(string).strip() not in ["None", ""]:
                userbot = Client(
                    name=f"AviaxAss{i}",
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    session_string=string.strip(),
                )
                call = PyTgCalls(userbot)
                self.clients.append(call)

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_group_call(chat_id)
        except:
            pass

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        language = await get_lang(chat_id)
        _ = get_string(language)

        stream = (
            AudioVideoPiped(link, HighQualityAudio(), MediumQualityVideo())
            if video
            else AudioPiped(link, HighQualityAudio())
        )

        try:
            await assistant.join_group_call(chat_id, stream)
        except NoActiveGroupCall:
            raise AssistantErr(_["call_8"])
        except AlreadyJoined:
            raise AssistantErr(_["call_9"])
        except TelegramServerError:
            raise AssistantErr(_["call_10"])

        await add_active_chat(chat_id)
        await music_on(chat_id)

    async def change_stream(self, client, chat_id):
        queue = db.get(chat_id)
        if not queue:
            await _clear_(chat_id)
            return await client.leave_group_call(chat_id)

        try:
            popped = queue.pop(0)
            await auto_clean(popped)

            next_file = queue[0]["file"]
            is_video = str(queue[0]["streamtype"]) == "video"

            stream = (
                AudioVideoPiped(next_file, HighQualityAudio(), MediumQualityVideo())
                if is_video
                else AudioPiped(next_file, HighQualityAudio())
            )

            await client.change_stream(chat_id, stream)
        except:
            pass

    async def start(self):
        LOGGER(__name__).info("Starting Assistant Clients...")
        for client in self.clients:
            await client.start()
            self._register_decorators(client)

    def _register_decorators(self, client: PyTgCalls):
        @client.on_stream_end()
        async def stream_end_handler(_, update: Update):
            if isinstance(update, StreamAudioEnded):
                await self.change_stream(client, update.chat_id)


Aviax = Call()


