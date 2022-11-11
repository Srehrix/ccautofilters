from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from info import ADMINS

@Client.on_message(filters.command('db_delete') & filters.user(ADMINS))
async def db_delete(bot, message):
    await message.reply_text(
        '**⚠️ Warning !! ❗ Read This Carefully. Otherwise Your Files will lost 🥶**\n\n1. **Select The Size**\n<i>It Will Delete Entire Files Below the Size</i>\n\n2. **This Will Remove all the files containing the below names**\n* <i>Theatre Prints, Website Names Such As Tamilmvu Tamilblasters, HTPMovies, etc.. & Subtitles</i>\n\n3. **This Will Remove all the files like**\n* <i>Images, Documents & Audio</i>',
        reply_markup=InlineKeyboardMarkup(
                  [[
            InlineKeyboardButton('Below 10 MB', callback_data='manuelfilter'), 
            InlineKeyboardButton('Below 30 MB', callback_data='autofilter'),
            InlineKeyboardButton('Below 50 MB', callback_data='autofilter')
        ], [
            InlineKeyboardButton('File Name', callback_data='autofilter'),
            InlineKeyboardButton('File Type', callback_data='autofilter')
        ], [
            InlineKeyboardButton('Cancel', callback_data='close_data')
        ],]
        ),
        quote=True,
    )

