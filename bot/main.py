from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils import executor

API_TOKEN = "YOUR_BOT_API_TOKEN"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

user_data = {}


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.reply("Hi!\nPlease enter your first name:")


@dp.message_handler(lambda message: "first_name" not in user_data)
async def process_first_name(message: types.Message):
    user_data["first_name"] = message.text
    await message.reply("Please enter your last name:")


@dp.message_handler(lambda message: "last_name" not in user_data)
async def process_last_name(message: types.Message):
    user_data["last_name"] = message.text
    await message.reply("Please enter your middle name:")


@dp.message_handler(lambda message: "middle_name" not in user_data)
async def process_middle_name(message: types.Message):
    user_data["middle_name"] = message.text
    await message.reply("Please enter your phone number:")


@dp.message_handler(lambda message: "phone_number" not in user_data)
async def process_phone_number(message: types.Message):
    user_data["phone_number"] = message.text
    await message.reply("Please enter your region:")


@dp.message_handler(lambda message: "region" not in user_data)
async def process_region(message: types.Message):
    user_data["region"] = message.text

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Most common questions"))
    markup.add(KeyboardButton("Disagree"))
    markup.add(KeyboardButton("Complain"))

    await message.reply("Please choose an option:", reply_markup=markup)


@dp.message_handler(
    lambda message: message.text in ["Most common questions", "Disagree", "Complain"]
)
async def process_button_choice(message: types.Message):
    user_data["chosen_button"] = message.text
    await message.reply(
        "Please provide a description:", reply_markup=ReplyKeyboardRemove()
    )


@dp.message_handler(lambda message: "description" not in user_data)
async def process_description(message: types.Message):
    user_data["description"] = message.text
    response = (
        f"First Name: {user_data['first_name']}\n"
        f"Last Name: {user_data['last_name']}\n"
        f"Middle Name: {user_data['middle_name']}\n"
        f"Phone Number: {user_data['phone_number']}\n"
        f"Region: {user_data['region']}\n"
        f"Chosen Button: {user_data['chosen_button']}\n"
        f"Description: {user_data['description']}"
    )
    await message.answer(response)


if __name__ == "__main__":
    executor.start_polling(dp)
