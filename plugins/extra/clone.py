import os
import re 
import sys
import asyncio 
import logging 

from database.users_chats_db import db
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message 
from pyrogram.errors.exceptions.bad_request_400 import AccessTokenExpired, AccessTokenInvalid
from pyrogram.errors import FloodWait 
from info import API_ID, API_HASH
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)]\[buttonurl:/{0,2}(.+?)(:same)?])")
BOT_TOKEN_TEXT = "<b>1) create a bot using @BotFather\n2) Then you will get a message with bot token\n3) Forward that message to me</b>"
SESSION_STRING_SIZE = 351

class CLIENT: 
  def __init__(self):
     self.api_id = API_ID
     self.api_hash = API_HASH
  def client(self, data, user=None):
     if user == None and data.get('is_bot') == False:
        data = data.get('token')
     return Client("BOT", self.api_id, self.api_hash, bot_token=data, in_memory=True)  
  
@Client.on_message(filters.forwarded & filters.private)
async def add_bot(self, message):
    user = int(message.from_user.id)
    if str(message.forward_from.id) != "93372553":
      return await message.reply_text("<b>process cancelled !</b>")
    bot_token = re.findall(r'\d[0-9]{8,10}:[0-9A-Za-z_-]{35}', message.text, re.IGNORECASE)
    match = bot_token[0] if bot_token else None
    if not match:
       return await message.reply_text("<b>There is no bot token in that message</b>")
