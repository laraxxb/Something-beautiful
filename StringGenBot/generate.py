from telethon import TelegramClient
from pyrogram.types import Message
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)

from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

from data import Data

api_ids = ["29508425"]
api_hashes = ["b78ee7cb7434667d1f1f121a1f509415"]

ask_ques = "اضغط للاستخراج !"
buttons_ques = [
    [
        ##InlineKeyboardButton("Pyrogram", callback_data="pyrogram"),
        InlineKeyboardButton("Telethon", callback_data="telethon")
    ]]##,
##    [
##        InlineKeyboardButton("Pyrogram Bot", callback_data="pyrogram_bot"),
 ##       InlineKeyboardButton("Telethon Bot", callback_data="telethon_bot"),
##    ],
##]


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if telethon:
        ty = "Telethon"
    else:
        ty = "Pyrogram v2"
    if is_bot:
        ty += " Bot"
    await msg.reply(f"{ty} يتم بدا استخراج جلسة...")
    user_id = msg.chat.id
    selected_index = 0 #random.randint(0, 1)
    api_id = api_ids[selected_index]
    api_hash = api_hashes[selected_index]
    if not is_bot:
        t = "**قم بإرسال رقم الهاتف الان مع مفتاح الدولة.\n +96612345678:مثل**"
    else:
        t = "Now please send your `BOT_TOKEN` \nExample : `12345:abcdefghijklmnopqrstuvwxyz`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("يتم إرسال رمز التحقق...")
    else:
        await msg.reply("Logging as Bot User...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name=f"bot_{user_id}", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name=f"user_{user_id}", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('`API_ID` and `API_HASH` combination is invalid. Please start generating session again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('رقم الهاتف غير صحيح، استخرج مرة اخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "الآن ارسل رمز التحقق الذي وصل لك من تيليجرام\n بالصيغة التالية\n 1234 --» 1 2 3 4\n عبر ترك مسافة بين كل رقم.", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply('Time limit reached of 10 minutes. Please start generating session again.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply('رمز التحقق غير صحيح، استخرج مرة اخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply('رمز التحقق منتهي الصلاحية!, استخرج مرة اخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await bot.ask(user_id, 'حسابك يستخدم التحقق بخطوتين، قم بارسال الرمز الان.', filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply('تم تجاوز الوقت المسموح به 5 دقائق، استخرج مرة اخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await two_step_msg.reply('الرمز غير صحيح، استخرج مرة اخرى', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**{ty.upper()} جلسة تيرمكس** \n\n`{string_session}` \n\nاستخرجت بواسطة @q9oebot\n**البوت غير تابع لسورس الجوكر!**"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "{} تم استخراج جلسة. \n\nتحقق من الرسائل المحفوظة! \n\nBy @q9o_e".format("telethon" if telethon else "pyrogram"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("تم الغاء العملية!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("تم اعادة التشغيل!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("تم الغاء العملية!", quote=True)
        return True
    else:
        return False
