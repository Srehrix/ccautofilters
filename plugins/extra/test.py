import os
import asyncio
import youtube_dl

from pornhub_api import PornhubApi
from pornhub_api.backends.aiohttp import AioHttpBackend
from youtube_dl.utils import DownloadError
from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
 


active = []
queues = []

@Client.on_inline_query("p")
async def inline_search(c: Client, q: InlineQuery):
    query = q.query
    backend = AioHttpBackend()
    api = PornhubApi(backend=backend)
    results = []
    try:
        src = await api.search.search(query)
    except ValueError as e:
        results.append(
            InlineQueryResultArticle(
                title="I can't found it!",
                description="The video can't be found, try again later.",
                input_message_content=InputTextMessageContent(
                    message_text="video not found!"
                ),
            ),
        )
        await q.answer(
            results,
            switch_pm_text="• Results •",
            switch_pm_parameter="start",
        )

        return


    videos = src.videos
    await backend.close()
    
    for vid in videos:

        try:
            pornstars = ", ".join(v for v in vid.pornstars)
            categories = ", ".join(v for v in vid.categories)
            tags = ", #".join(v for v in vid.tags)
        except:
            pornstars = "N/A"
            categories = "N/A"
            tags = "N/A"
        capt = (f"Title: `{vid.title}`\n"
                f"Duration: `{vid.duration}`\n"
                f"Views: `{vid.views}`\n\n"
                f"**{pornstars}**\n"
                f"Category: {categories}\n\n"
                f"{tags}"
                f"Link: {vid.url}")

        text = f"{vid.url}"

        results.append(
            InlineQueryResultArticle(
                title=vid.title,
                input_message_content=InputTextMessageContent(
                    message_text=text, disable_web_page_preview=True,
                ),
                description=f"Duration: {vid.duration}\nViews: {vid.views}\nRating: {vid.rating}",
                thumb_url=vid.thumb,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("watch in web", url=vid.url),
                        ],
                    ],
                ),
            ),
        )

    await q.answer(
        results,
        switch_pm_text="• Results •",
        switch_pm_parameter="start",
    )
