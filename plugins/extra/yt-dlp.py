@Client.on_message(url_filter)
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
                thumb="downloads/src/pornhub.jpeg",
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

