import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

API_TOKEN = "6195275934:AAEngBypgfNw3SwcV9uV_jdatZtMvojF9cs"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

user_data = {}
region_callback = CallbackData("region", "name")
option_callback = CallbackData("option", "name")
uzbekistan_regions = [
    "Andijan",
    "Bukhara",
    "Fergana",
    "Jizzakh",
    "Khorezm",
    "Namangan",
    "Navoiy",
    "Qashqadaryo",
    "Samarkand",
    "Sirdaryo",
    "Surkhandarya",
    "Tashkent",
    "Tashkent City",
    "Karakalpakstan",
]


def is_user_in_database(telegram_id):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    if is_user_in_database(message.from_user.id):
        await present_options(message)
    else:
        user_data[message.from_user.id] = {}
        await message.reply("Hi!\nPlease enter your first name:")


async def present_options(message: types.Message):
    inline_kb = InlineKeyboardMarkup(row_width=3)
    inline_kb.add(
        InlineKeyboardButton("FAQ", callback_data=option_callback.new(name="FAQ"))
    )
    inline_kb.add(
        InlineKeyboardButton(
            "Categories", callback_data=option_callback.new(name="Categories")
        )
    )
    inline_kb.add(
        InlineKeyboardButton("Back", callback_data=option_callback.new(name="Back"))
    )
    await message.reply("Please select an option:", reply_markup=inline_kb)


@dp.message_handler(
    lambda message: "first_name" not in user_data.get(message.from_user.id, {})
)
async def process_first_name(message: types.Message):
    user_data[message.from_user.id] = {"first_name": message.text}
    await message.reply("Please enter your last name:")


@dp.message_handler(
    lambda message: "last_name" not in user_data.get(message.from_user.id, {})
)
async def process_last_name(message: types.Message):
    user_data[message.from_user.id]["last_name"] = message.text
    await message.reply("Please enter your middle name:")


@dp.message_handler(
    lambda message: "middle_name" not in user_data.get(message.from_user.id, {})
)
async def process_middle_name(message: types.Message):
    user_data[message.from_user.id]["middle_name"] = message.text
    await message.reply("Please enter your phone number:")


@dp.message_handler(
    lambda message: "phone_number" not in user_data.get(message.from_user.id, {})
)
async def process_phone_number(message: types.Message):
    user_data[message.from_user.id]["phone_number"] = message.text
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for region in uzbekistan_regions:
        inline_kb.add(
            InlineKeyboardButton(region, callback_data=region_callback.new(name=region))
        )
    await message.reply("Please choose your region:", reply_markup=inline_kb)


@dp.callback_query_handler(region_callback.filter())
async def process_region_selection(query: types.CallbackQuery, callback_data: dict):
    region = callback_data["name"]
    user_data[query.from_user.id]["region"] = region
    await present_options(query.message)


@dp.callback_query_handler(option_callback.filter())
async def process_option_selection(query: types.CallbackQuery, callback_data: dict):
    option = callback_data["name"]
    await query.message.reply(f"You selected {option}.")
    await query.answer()


@dp.message_handler(lambda message: message.text in ["FAQ", "Categories", "Back"])
async def process_query_options(message: types.Message):
    await message.reply(f"You pressed the {message.text} button.")


@dp.message_handler(
    lambda message: "description" not in user_data.get(message.from_user.id, {})
)
async def process_description(message: types.Message):
    user_data[message.from_user.id]["description"] = message.text
    data = user_data[message.from_user.id]
    response = (
        f"First Name: {data['first_name']}\n"
        f"Last Name: {data['last_name']}\n"
        f"Middle Name: {data['middle_name']}\n"
        f"Phone Number: {data['phone_number']}\n"
        f"Region: {data['region']}\n"
        f"Description: {data.get('description', 'Not provided')}"
    )
    await message.answer(response)


if __name__ == "__main__":
    executor.start_polling(dp)
