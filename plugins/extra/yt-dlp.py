import os
import asyncio
import youtube_dl
import threading

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
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden, MessageNotModified, FloodWait

log_chat: int = -1761918450
sub_chat: str = "vysakh_xd"

def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def edit_msg(client, message, to_edit):
    try:
        client.loop.create_task(message.edit(to_edit))
    except MessageNotModified:
        pass
    except FloodWait as e:
        client.loop.create_task(asyncio.sleep(5))
    except TypeError:
        pass


def download_progress_hook(d, message, client):
    if d['status'] == 'downloading':
        current = d.get("_downloaded_bytes_str") or humanbytes(int(d.get("downloaded_bytes", 1)))
        total = d.get("_total_bytes_str") or d.get("_total_bytes_estimate_str")
        file_name = d.get("filename")
        eta = d.get('_eta_str', "N/A")
        percent = d.get("_percent_str", "N/A")
        speed = d.get("_speed_str", "N/A")
        to_edit = f"📥 <b>Downloading!</b>\n\n<b>Name :</b> <code>{file_name}</code>\n<b>Size :</b> <code>{total}</code>\n<b>Speed :</b> <code>{speed}</code>\n<b>ETA :</b> <code>{eta}</code>\n\n<b>Percentage: </b> <code>{current}</code> from <code>{total} (__{percent}__)</code>"
        threading.Thread(target=edit_msg, args=(client, message, to_edit)).start()

if os.path.exists("downloads"):
    print("✅ file is exist")
else:
    print("✅ file has made")


active = []
queues = []

async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


@Client.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def options(c: Client, m: Message):
    print(m.text)
    await m.reply_text(
        "Tap the button to continue action!", 
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Download", callback_data=f"d_{m.text}",
                    ),
                ],[
                    InlineKeyboardButton(
                        "watch in web", url=m.text,
                    ),
                ],
            ],
        ),
    )


@Client.on_callback_query(filters.regex("^d"))
async def get_video(c: Client, q: CallbackQuery):
    url = q.data.split("_",1)[1]
    msg = await q.message.edit("Downloading...")
    user_id = q.message.from_user.id

    if "some" in active:
        await q.message.edit("Sorry, you can only download videos at a time!")
        return
    else:
        active.append(user_id)

    ydl_opts = {
            "progress_hooks": [lambda d: download_progress_hook(d, q.message, c)]
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            await run_async(ydl.download, [url])
        except DownloadError:
            await q.message.edit("Sorry, an error occurred")
            return


    for file in os.listdir('.'):
        if file.endswith(".mp4"):
            await q.message.reply_video(
                f"{file}",
                thumb="assets/logo.jpg",
                width=1280,
                height=720,
                caption="The content you requested has been successfully downloaded!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("• Donate •", url="https://trakteer.id/levina-crqid/tip"),
                        ],
                    ],
                ),
            )
            os.remove(f"{file}")
            break
        else:
            continue
    
   
    await msg.delete() 
    active.remove(user_id)

