from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from info import ADMINS
from database.ia_filterdb import Media

@Client.on_message(filters.command('db_delete'))
async def db_delete(bot, message):
    buttons = [[
            InlineKeyboardButton('Below 10 MB', callback_data='dlta'), 
            InlineKeyboardButton('Below 30 MB', callback_data='dltb'),
            InlineKeyboardButton('Below 50 MB', callback_data='dltc')
            ], [
            InlineKeyboardButton('File Name', callback_data='dltname'),
            InlineKeyboardButton('File Type', callback_data='dlttype')
            ], [
            InlineKeyboardButton('Delete All Files', callback_data='dltall')
            ], [
            InlineKeyboardButton('Cancel', callback_data='close_data')
            ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text="**⚠️ Warning !! ❗ Read This Carefully, Otherwise Your Files will lost 🥶**\n\n1. **Select The Size**\n<i>It Will Delete Entire Files Below the Size</i>\n\n2. **This Will Remove all the files containing the below names**\n* <i>Theatre Prints, Website Names Such As Tamilmvu Tamilblasters, HTPMovies, etc.. & Subtitles</i>\n\n3. **This Will Remove all the files like**\n* <i>Images, Documents & Audio</i>",
        reply_markup=reply_markup)

@Client.on_callback_query(filters.regex('dlta'))
async def dlta(bot, message):
    buttons = [[
            InlineKeyboardButton('Yes', callback_data='dlt_a'),
            InlineKeyboardButton('No', callback_data='db_delete')
        ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.message.edit_text(
        text="This will delete all files below 10MB.\nDo you want to continue??",
        reply_markup=reply_markup)

@Client.on_callback_query(filters.regex('dltb'))
async def dltb(bot, message):
    buttons = [[
            InlineKeyboardButton('Yes', callback_data='dlt_b'),
            InlineKeyboardButton('No', callback_data='db_delete')
        ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.edit_text(
        text="This will delete all files below 30MB.\nDo you want to continue??",
        reply_markup=reply_markup)

@Client.on_callback_query(filters.regex('dltc'))
async def dltc(bot, message):
    buttons = [[
            InlineKeyboardButton('Yes', callback_data='dlt_c'),
            InlineKeyboardButton('No', callback_data='db_delete')
        ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text="This will delete all files below 50MB.\nDo you want to continue??",
        reply_markup=reply_markup)

@Client.on_callback_query(filters.regex('dltall'))
async def dltall(bot, message):
    buttons = [[
            InlineKeyboardButton('Yes', callback_data='dlt_all'),
            InlineKeyboardButton('No', callback_data='db_delete')
        ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text="This will delete all files.\nDo you want to continue??",
        reply_markup=reply_markup)

@Client.on_callback_query(filters.regex('dlt_all'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer('Piracy Is Crime')
    await message.message.edit('Succesfully Deleted All The Indexed Files.')
