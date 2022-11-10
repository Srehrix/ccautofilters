from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Client.on_message(filters.command('db_delete') & filters.user(ADMINS))
async def db_delete(bot, message):
    await message.reply_text(
        'Do you want to continue??',
        reply_markup=InlineKeyboardMarkup(
                  [[
            InlineKeyboardButton('Below 10 MB', callback_data='manuelfilter'), 
            InlineKeyboardButton('Below 30 MB', callback_data='autofilter'),
            InlineKeyboardButton('Below 50 MB', callback_data='autofilter')
        ], [
            InlineKeyboardButton('Cancel', callback_data='autofilter')
        ]]
