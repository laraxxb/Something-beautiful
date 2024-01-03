from pyrogram.types import InlineKeyboardButton
import env

class Data:
    generate_single_button = [InlineKeyboardButton("↯︙ انشاء كود بايروجرام .", callback_data="generate")]

    generate_button = [generate_single_button]

    buttons = [
        generate_single_button,
        [InlineKeyboardButton("↯︙المطور .", url=f"https://t.me/{env.DEV}"),
        ],
    ]

    START = """
↯︙اهلا بك في بوت انشاء كود بايروجرام .

↯︙ يمكنك انشاء كود بايروجرام بسهولة .

↯︙يتم ارسال الكود في الرسائل المحفوضة .
    """
