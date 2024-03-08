import re
import os
import io
import logging

from PyXDBot.pyxdbot import PyXDTelebot
from PyXDBot.logger import setup_logging
from telebot import types, async_telebot
from datetime import datetime
from typing import Any
from dotenv import load_dotenv

class XTelebot(PyXDTelebot):
    def __init__(self):
        '''
        XTelebot is a Telegram bot created using the Python programming language,
        specifically designed to facilitate the seamless sharing of media such as photos and videos from Twitter user posts.
        The bot leverages the Twitter API to extract multimedia content from a user's post and swiftly deliver it automatically to users through the Telegram platform.
        '''
        super().__init__()
        load_dotenv()

        TOKEN = os.environ.get("TELEBOT_TOKEN")
        self.bot = async_telebot.AsyncTeleBot(token=TOKEN)

        self.func_name = None
        self.is_stop = False
        self.message_id = None
        self.is_click = 0
        self.medias = []
        self.cursor = None
        self.msg_text = ""

        self.delws = lambda text: re.sub(r'\s', '', text)
        self.instructions = lambda chat_id: self.bot.send_message(chat_id=chat_id, text=f"Unrecognized command. Say what?")

        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)

        @self.bot.message_handler(commands=["start"])
        async def introduction(message):
            id = message.chat.id
            username = message.from_user.username

            await self.bot.reply_to(message, f"Welcome👋, {username}")
            await self.bot.send_message(
                chat_id=id,
                text="If you are still confused when using this <a href='https://t.me/itsPyXD_bot'>bot</a>, see /help.",
                parse_mode="HTML"
            )
        
        @self.bot.message_handler(commands=["stop"])
        async def stop_generate(message):
            self.is_stop = True

        @self.bot.message_handler(commands=["help"])
        async def helper(message):
            id = message.chat.id

            await self.bot.send_message(
                chat_id=id,
                text=(
                    "I can help you using this <b>PyXDTelebot</b>.\n"
                    "You can control me by sending these commands :\n\n"
                    "/start - Starting the <a href='https://t.me/itsPyXD_bot'>bot</a>\n"
                    "/features - Shows the features of this bot.\n"
                    "/stop - Stops media delivery.\n\n"
                    "📖 Description of features:\n"
                    "   ✮ <i>All Media</i> - Images and Videos from Twitter user posts.\n"
                    "   ✮ <i>Images</i> - Images from Twitter user posts.\n"
                    "   ✮ <i>Videos</i> - Videos from Twitter user posts.\n"
                    "   ✮ <i>Link Downloader</i> - Media form the given URL.\n\n"
                    "😱 Implementation of each feature :\n"
                    "   ✮ <i>All Media, Images, Videos</i> :\n"
                    "       ○ Complete this :\n"
                    "           screen_name = <b>(Required)</b>\n"
                    "           cursor = <b>(Optional)</b>\n"
                    "       ○ Application example :\n"
                    "           screen_name = iam_muhfalihr\n"
                    "         -------------------- or --------------------\n"
                    "           screen_name = iam_muhfalihr\n"
                    "           cursor = AbCdFgH___iJkLmNoPq\n\n"
                    "   ✮ <i>Link Downloader</i> :\n"
                    "       Send Twitter User Post link!\n\n"
                    "Please use this bot happily and calmly.\n"
                    "Greetings of peace from @muhammadfalihromadhoni 💙\n\n"
                    "🌟 Follow my Github <a href='https://github.com/muhfalihr'>muhfalihr</a>\n"
                    "🚀 Follow my Instagram <a href='https://www.instagram.com/_____mfr.py/'>@_____mfr.py</a>"
                ),
                parse_mode="HTML"
            )
        
        @self.bot.message_handler(commands=["features"])
        async def inline_key_button(message):
            id = message.chat.id
            
            markup = types.InlineKeyboardMarkup()
            allmedia = types.InlineKeyboardButton("All Media", callback_data="All Media")
            images = types.InlineKeyboardButton("Images", callback_data="Images")
            videos = types.InlineKeyboardButton("Videos", callback_data="Videos")
            linkdownloader = types.InlineKeyboardButton("Link Downloader", callback_data="Link Downloader")

            markup.add(allmedia, images, videos, linkdownloader)

            await self.bot.send_message(chat_id=id, text="🧐 Select one of the downloader features:", reply_markup=markup)

        @self.bot.callback_query_handler(func=lambda call: True if call.data in  ["All Media", "Images", "Videos", "Link Downloader"] else False)
        async def option(call):
            id = call.message.chat.id
            call_data = call.data
            self.is_click += 1

            if call_data in ["All Media", "Images", "Videos"]:
                self.func_name = call_data
                text = (
                        f"<i><b>{call_data} Feature</b></i>\n"
                        "OK. Complete this!.\n\n"
                        "<code>screen_name = (Required)</code>\n"
                        "<code>cursor = (Optional)</code>\n\n"
                        "Confused? See /help."
                    )
            else:
                self.func_name = call_data
                text = (
                        "OK. Send Twitter User Post link!.\n"
                        "Confused? See /help."
                    )

            if self.is_click > 1:
                message = await self.bot.edit_message_text(chat_id=id, message_id=self.message_id, text=text, parse_mode="HTML")
                self.message_id = message.message_id
            else:
                message = await self.bot.send_message(chat_id=id, text=text, parse_mode="HTML")
                self.message_id = message.message_id
        
        @self.bot.callback_query_handler(func=lambda call: True if call.data in ["yes", "no"] else False)
        async def is_continue(call):
            id = call.message.chat.id
            call_data = call.data
            message_id = call.message.message_id

            match call_data:
                case "yes":
                    self.is_stop = False
                    await self.bot.edit_message_text(chat_id=id, message_id=message_id, reply_markup=None, text="🟢 Continue sending media...")
                    await self.__media_processor(id=id)
                case "no":
                    self.is_stop = False
                    await self.bot.edit_message_text(chat_id=id, message_id=message_id, reply_markup=None, text="OK, if you don't want to continue. /features")
                    self.is_click = 0
        
        @self.bot.message_handler(commands=["report"])
        async def report(message):
            await self.bot.send_message(
                chat_id=message.chat.id,
                text=(
                    "Report a Problem 🙏 : ...\n\n"
                    "Copy and complete the report text above."
                )
            )

        @self.bot.message_handler(func=lambda message: True if re.match(pattern=r'[Rr]eport.+:.+', string=message.text) else False)
        async def savereport(message):
            id = message.chat.id
            user = message.from_user.username

            if "report" not in os.listdir(self.__pathdir): self.__mkdir(folder_name="report")

            with open(f"report/{user}{datetime.now().strftime('%Y%m%d%H%M%S')}.txt", "w") as report_file:
                report_file.write(message.text)

            await self.bot.send_message(chat_id=id,text="Report sent successfully. Thank you🙏. /help")

        
        @self.bot.message_handler(func=lambda message: True if self.func_name in ["All Media", "Images", "Videos", "Link Downloader"] and message.text else False)
        async def media_sender(message):
            self.logger.info(f"Download media with features {self.func_name}")
            
            id = message.chat.id
            msg = message.text
            parameters = dict()

            if re.match(pattern=r'(screen_name|cursor) = .+', string=msg):
                parameters.update({"features": self.func_name})

                for param in msg.split("\n"):
                    parameter = self.delws(param).split("=")
                    parameters.update({parameter[0]: parameter[1], "features": self.delws(self.func_name.lower())})
                
                await self.bot.send_message(
                    chat_id=id,
                    text=(
                        "Please Wait....\n"
                        f"🟢 This process may take a {'little' if self.func_name != 'Videos' else 'long'} time so please be patient and wait until the notification message appears."
                    )
                )

            elif re.match(pattern=r'https://(?:www\.)?x\.com/\w+/status/\d+\?s=\d+', string=msg):
                await self.bot.send_message(
                    chat_id=id,
                    text="🟢 Please Wait...."
                )

                pattern = re.compile(r'/([^/?]+)\?')
                matches = pattern.search(msg)
                if matches:
                    focalTweetId = matches.group(1)
                    parameters.update({"focalTweetId": focalTweetId, "features": "tweetdetail"})
                else:
                    self.instructions(chat_id=id)

            else:
                await self.instructions(chat_id=id)
            
            try:
                medias, cursor = self.media_url_getter(**parameters)

                self.medias = medias
                self.cursor = cursor
                self.msg_text = msg

                await self.__media_processor(id=id)
                
            except Exception:
                await self.__http_error(chat_id=id)
        
    async def __media_processor(self, id: str) -> Any:
        '''
        Media processing that will be sent to Telegram users

        Arguments :
          - id (Required): message.chat.id
        '''
        medias_copy = list(self.medias)
        self.medias.pop(0)

        media_group = []
        for media in medias_copy:
            if self.is_stop: break

            data, filename, content_type = self.download(media)

            databyte = io.BytesIO(data)
            databyte.name = filename

            match self.func_name:
                case "All Media" | "Videos":
                    if len(media_group) == 3: media_group.clear()

                    if len(media_group) < 3:
                        if "image" in content_type:
                            media_group.append(types.InputMediaPhoto(media=databyte))
                        if "video" in content_type:
                            media_group.append(types.InputMediaVideo(media=databyte))
                    
                    self.logger.info(f"Sending media in the form of {content_type} to users.")
                    
                    try:
                        if len(media_group) == 3:
                            await self.bot.send_media_group(chat_id=id, media=media_group, timeout=60)
                    except Exception:
                        await self.bot.send_message(chat_id=id, text="😥 Failed to send media.")

                case "Images":
                    if len(media_group) == 5: media_group.clear()

                    if len(media_group) < 5:
                        media_group.append(types.InputMediaPhoto(media=databyte))
                    
                    self.logger.info(f"Sending media in the form of {content_type} to users.")

                    try:
                        if len(media_group) == 5:
                            await self.bot.send_media_group(chat_id=id, media=media_group, timeout=60)
                    except Exception:
                        await self.bot.send_message(chat_id=id, text="😥 Failed to send media.")
                
                case "Link Downloader":
                    if len(media_group) == 5: media_group.clear()

                    if len(media_group) < 5:
                        if "image" in content_type:
                            media_group.append(types.InputMediaPhoto(media=databyte))

                        elif "video" in content_type:
                            media_group.append(types.InputMediaVideo(media=databyte))
                        
                        self.logger.info(f"Sending media in the form of {content_type} to users.")

                    try:
                        if len(media_group) == 5:
                            await self.bot.send_media_group(chat_id=id,media=media_group, timeout=60)
                    except Exception:
                        await self.bot.send_message(chat_id=id, text="😥 Failed to send media.")

        try:
            if media_group: await self.bot.send_media_group(chat_id=id,media=media_group)
        except Exception: pass

        if self.is_stop:
            await self.bot.send_message(chat_id=id, text=f"🛑 Stops media delivery...")
            self.func_name = self.func_name

            markup = types.InlineKeyboardMarkup()
            yes = types.InlineKeyboardButton("Yes", callback_data='yes')
            no = types.InlineKeyboardButton("No", callback_data='no')
            
            markup.add(yes, no)
            await self.bot.send_message(chat_id=id, text="🧐 Do you want to continue?", reply_markup=markup)
            self.medias = self.medias
        else:
            if self.cursor:
                await self.bot.send_message(
                    chat_id=id,
                    text=(
                        f"Your previous message : \n<code>{self.msg_text}</code>\n\n"
                        f"Cursor for next media: \n<code>cursor = {self.cursor}</code>"
                    ),
                    parse_mode="HTML"
                )
                self.is_click = 0
            else:
                await self.bot.send_message(chat_id=id, text="Done 😊")
                self.func_name = None
                self.is_click = 0

            await self.bot.send_message(chat_id=id,text="To continue or not, specify in /features.")


    async def __http_error(self, chat_id: str) -> Any:
        '''
        Handling errors by sending errors to the user to report

        Arguments:
          - chat_id (Required): message.chat.id
        '''
        if self.http_error_reason and self.http_error_status_code is not None:
            await self.bot.send_message(
                chat_id=chat_id,
                text=f"❌ Error! status code {self.http_error_reason} : {self.http_error_status_code}"
            )
            await self.bot.send_message(chat_id=chat_id, text="Sorry🙏 Please report this issue. /report")
        else:
            await self.bot.send_message(chat_id=chat_id, text=f"❌ Error! A request to the Telegram API was unsuccessful.")
            await self.bot.send_message(chat_id=chat_id, text="Sorry🙏 Please Try Again 😥. /report")

    async def start_polling(self) -> None:
        '''
        Starting the PyXDTelebot program

        ---
        '''
        self.logger.info("Starting the PyXDTelebot program has gone well.")
        await self.bot.polling(non_stop=True)