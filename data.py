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
- مَـرحـبـاً بك فـي بـوت استخـراج كـود تيرمكـس💫
- يعمـل هـذا البـوت لمساعدتـك بطريقـة سهلـه 🏂
- للحصـول على كـود تيرمكـس بـدون بـانـد🎗
    """
