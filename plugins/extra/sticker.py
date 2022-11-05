import imghdr
import os
from typing import List
from asyncio import gather

from pyrogram import filters, Client, errors, raw
from pyrogram.errors import (
    PeerIdInvalid,
    ShortnameOccupyFailed,
    StickerEmojiInvalid,
    StickerPngDimensions,
    StickerPngNopng,
    UserIsBlocked,
)


MAX_STICKERS = (
    120  # would be better if we could fetch this limit directly from telegram
)
SUPPORTED_TYPES = ["jpeg", "png", "webp"]


async def get_sticker_set_by_name(
        client: Client, name: str
) -> raw.base.messages.StickerSet:
    try:
        return await client.send(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=name),
                hash=0,
            )
        )
    except errors.exceptions.not_acceptable_406.StickersetInvalid:
        return None


# Known errors: (I don't see a reason to catch them as we, for sure, won't face them right now):
# errors.exceptions.bad_request_400.PackShortNameInvalid -> pack name needs to end with _by_botname
# errors.exceptions.bad_request_400.ShortnameOccupyFailed -> pack's name is already in use


async def create_sticker_set(
        client: Client,
        owner: int,
        title: str,
        short_name: str,
        stickers: List[raw.base.InputStickerSetItem],
) -> raw.base.messages.StickerSet:
    return await client.send(
        raw.functions.stickers.CreateStickerSet(
            user_id=await client.resolve_peer(owner),
            title=title,
            short_name=short_name,
            stickers=stickers,
        )
    )


async def add_sticker_to_set(
        client: Client,
        stickerset: raw.base.messages.StickerSet,
        sticker: raw.base.InputStickerSetItem,
) -> raw.base.messages.StickerSet:
    return await client.send(
        raw.functions.stickers.AddStickerToSet(
            stickerset=raw.types.InputStickerSetShortName(
                short_name=stickerset.set.short_name
            ),
            sticker=sticker,
        )
    )


async def create_sticker(
        sticker: raw.base.InputDocument, emoji: str
) -> raw.base.InputStickerSetItem:
    return raw.types.InputStickerSetItem(document=sticker, emoji=emoji)

@Client.on_message(filters.command("kang"))
async def kang(client, message: Message):
    BOT_USERNAME = client.username
    if not message.reply_to_message:
        return await message.reply_text("Reply to a sticker/image to kang it.")
    if not message.from_user:
        return await message.reply_text(
            "You are anon admin, kang stickers in my pm."
        )
    msg = await message.reply_text("Kanging Sticker..")

    # Find the proper emoji
    args = message.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    elif (
            message.reply_to_message.sticker
            and message.reply_to_message.sticker.emoji
    ):
        sticker_emoji = message.reply_to_message.sticker.emoji
    else:
        sticker_emoji = "😎"

    # Get the corresponding fileid, resize the file if necessary
    doc = message.reply_to_message.photo or message.reply_to_message.document
    try:
        if message.reply_to_message.sticker:
            sticker = await create_sticker(
                await get_document_from_file_id(
                    message.reply_to_message.sticker.file_id
                ),
                sticker_emoji,
            )
        elif doc:
            if doc.file_size > 10000000:
                return await msg.edit("File size too large.")

            temp_file_path = await client.download_media(doc)
            image_type = imghdr.what(temp_file_path)
            if image_type not in SUPPORTED_TYPES:
                return await msg.edit(
                    "Format not supported! ({})".format(image_type)
                )
            try:
                temp_file_path = await resize_file_to_sticker_size(
                    temp_file_path
                )
            except OSError as e:
                await msg.edit_text("Something wrong happened.")
                raise Exception(
                    f"Something went wrong while resizing the sticker (at {temp_file_path}); {e}"
                )
            sticker = await create_sticker(
                await upload_document(client, temp_file_path, message.chat.id),
                sticker_emoji,
            )
            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)
        else:
            return await msg.edit("Nope, can't kang that.")
    except ShortnameOccupyFailed:
        await message.reply_text("Change Your Name Or Username")
        return

    except Exception as e:
        await message.reply_text(str(e))
        e = format_exc()
        return print(e)
     
    # Find an available pack & add the sticker to the pack; create a new pack if needed
    # Would be a good idea to cache the number instead of searching it every single time...
    packnum = 0
    packname = "f" + str(message.from_user.id) + "_by_" + BOT_USERNAME
    limit = 0
    try:
        while True:
            # Prevent infinite rules
            if limit >= 50:
                return await msg.delete()

            stickerset = await get_sticker_set_by_name(client, packname)
            if not stickerset:
                stickerset = await create_sticker_set(
                    client,
                    message.from_user.id,
                    f"{message.from_user.first_name[:32]}'s | @BETA_BOTZ Pack",
                    packname,
                    [sticker],
                )
            elif stickerset.set.count >= MAX_STICKERS:
                packnum += 1
                packname = (
                        "f"
                        + str(packnum)
                        + "_"
                        + str(message.from_user.id)
                        + "_by_"
                        + BOT_USERNAME
                )
                limit += 1
                continue
            else:
                try:
                    await add_sticker_to_set(client, stickerset, sticker)
                except StickerEmojiInvalid:
                    return await msg.edit("[ERROR]: INVALID_EMOJI_IN_ARGUMENT")
            limit += 1
            break

        await msg.edit(
            "Sticker Kanged To [Pack](t.me/addstickers/{})\nEmoji: {}".format(
                packname, sticker_emoji
            )
        )
    except (PeerIdInvalid, UserIsBlocked):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Start", url=f"t.me/{BOT_USERNAME}")]]
        )
        await msg.edit(
            "You Need To Start A Private Chat With Me.",
            reply_markup=keyboard,
        )
    except StickerPngNopng:
        await message.reply_text(
            "Stickers must be png files but the provided image was not a png"
        )
    except StickerPngDimensions:
        await message.reply_text("The sticker png dimensions are invalid.")


