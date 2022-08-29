from pyrogram import Client, filters 
from pyrogram.types import User, Message
import time 
import os 
from info import ADMINS 

@Client.on_message(filters.private & filters.command(["forward"]))
async def forward(bot: Client, m: Message): 
    msg = await m.reply_text("**Forward any message from the Target channel\nBot should be admin at both the Channels**")
    t_chat = msg.forward_from_chat 
    msg1 = await photo.reply_text("**Send Starting Message From Where you want to Start forwarding**")
    msg2 = await document.reply_text("**Send Ending Message from same chat**")
    # print(msg1.forward_from_message_id, msg1.forward_from_chat.id, msg1.forward_from_message_id) 
    i_chat = msg1.forward_from_chat
    s_msg = int(msg1.forward_from_message_id)
    f_msg = int(msg2.forward_from_message_id)+1 
    await m.reply_text('**Forwarding Started**\n\nPress /restart to Stop and /log to get log TXT file') 
    try:      
        for i in range(s_msg, f_msg):
            try:
                await bot.copy_message(
                    chat_id= t_chat,
                    from_chat_id= i_chat,
                    message_id= i
                ) 
                time.sleep(2)
            except Exception: 
                continue 
    except Exception as e: 
        await m.reply_text(str(e)) 
    await m.reply_text("Done Forwarding")
