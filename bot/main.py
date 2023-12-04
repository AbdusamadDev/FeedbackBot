from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import BoundFilter
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
import sqlite3


# user_id = 2003049919
ADMIN_IDS = [2003049919]
API_TOKEN = "6195275934:AAEngBypgfNw3SwcV9uV_jdatZtMvojF9cs"
user_data = {}
option_callback = CallbackData("option", "name")
faq_callback = CallbackData("faq", "id")
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
region_callback = CallbackData("region", "name")
admin_response_state = {}


class UserIsAdminFilter(BoundFilter):
    key = "user_is_admin"

    def __init__(self, user_is_admin):
        self.user_is_admin = user_is_admin

    async def check(self, message: types.Message):
        user_is_admin = message.from_user.id in ADMIN_IDS
        return user_is_admin


dp.filters_factory.bind(UserIsAdminFilter)


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    middle_name = State()
    phone_number = State()
    region = State()


def fetch_question_text(question_id):
    """
    Fetch the question text from the database using the question ID.
    """
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT text FROM api_question WHERE id = ?", (question_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def get_user_telegram_id_from_question(question_id):
    """
    Get the Telegram ID of the user who asked the question.
    """
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT telegram_id FROM api_user JOIN api_question ON api_user.id = api_question.user_id WHERE api_question.id = ?",
        (question_id,),
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def save_answer_to_database(question_id, answer, admin_id):
    """
    Save the admin's answer to the `api_answer` table.
    """
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO api_answer (question_id, text, admin_id)
        VALUES (?, ?, ?)
        """,
        (question_id, answer, admin_id),
    )
    print("Somehtisdfasdfsdafdf")
    conn.commit()
    conn.close()


def create_new_question(text, status, category_id, user_id):
    """
    Create a new question in the SQLite3 database.
    """
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO api_question (text, status, category_id, user_id)
        VALUES (?, ?, ?, ?)
    """,
        (text, status, category_id, user_id),
    )
    conn.commit()
    conn.close()


def get_user_database_id(telegram_id):
    """
    Retrieve the user's database ID based on their Telegram ID using SQLite.
    """
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM api_user WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None


def fetch_unanswered_questions():
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM api_question WHERE status = 0")
    questions = cursor.fetchall()
    conn.close()
    return questions


def fetch_categories():
    """
    Fetch all categories from the database.
    """
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM api_category")
    categories = cursor.fetchall()
    conn.close()
    return [category[0] for category in categories]


def add_user_to_database(user_data):
    """
    Adds a user to the database using the provided user data.
    """
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    fullname = f"{user_data['first_name']} {user_data.get('middle_name', '')} {user_data['last_name']}".strip()
    phone_number = user_data["phone_number"]
    region = user_data["region"]
    telegram_id = user_data["telegram_id"]
    telegram_username = user_data.get("telegram_username", "")
    cursor.execute(
        """
        INSERT INTO api_user (fullname, phone_number, region, telegram_id, telegram_username) 
        VALUES (?, ?, ?, ?, ?)
    """,
        (fullname, phone_number, region, telegram_id, telegram_username),
    )
    conn.commit()
    conn.close()


def fetch_regions():
    """
    Fetch all regions from the database.
    """
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM api_regions")
    regions = cursor.fetchall()
    conn.close()
    return [region[0] for region in regions]


def is_user_in_database(telegram_id):
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_user WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def fetch_faqs():
    """
    Fetch all FAQ entries from the database.
    """
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM api_faq")
    faqs = cursor.fetchall()
    conn.close()
    return faqs


def fetch_faq_answer(faq_id):
    """
    Fetch the answer for a specific FAQ from the database.
    """
    conn = sqlite3.connect("../db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM api_faq WHERE id = ?", (faq_id,))
    answer = cursor.fetchone()
    conn.close()
    return answer[0] if answer else "No answer found."


def waiting_for_admin_response_condition(message: types.Message):
    user_id = message.from_user.id
    return admin_response_state.get(user_id, {}).get("awaiting_response", False)


######################################################################################
######################################################################################
######################################################################################
######################################################################################
# ------------------------- USER POSSIBLE ACTIONS ---------------------------
@dp.callback_query_handler(option_callback.filter(name="FAQ"))
async def process_faq_option(query: types.CallbackQuery):
    faqs = fetch_faqs()
    for faq_id, question in faqs:
        inline_kb = InlineKeyboardMarkup()
        inline_kb.add(
            InlineKeyboardButton(
                "See Answer", callback_data=faq_callback.new(id=faq_id)
            )
        )
        await query.message.reply(question, reply_markup=inline_kb)
    await query.answer()


@dp.callback_query_handler(faq_callback.filter())
async def process_faq_answer(query: types.CallbackQuery, callback_data: dict):
    faq_id = int(callback_data["id"])
    answer = fetch_faq_answer(faq_id)
    await query.message.reply(answer)
    await query.answer()


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


@dp.message_handler(commands=["start"], state=None)
async def process_start_command(message: types.Message, state: FSMContext):
    if is_user_in_database(message.from_user.id):
        await message.reply("What questions do you have today?")
        await present_options(message)
    else:
        await Registration.first_name.set()
        await message.reply("Hi!\nPlease enter your first name:")


@dp.message_handler(state=Registration.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["first_name"] = message.text
    await Registration.next()
    await message.reply("Please enter your last name:")


@dp.message_handler(state=Registration.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["last_name"] = message.text
    await Registration.next()
    await message.reply("Please enter your middle name:")


@dp.message_handler(state=Registration.middle_name)
async def process_middle_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["middle_name"] = message.text
    await Registration.next()
    await message.reply("Please enter your phone number:")


@dp.message_handler(state=Registration.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone_number"] = message.text
    await Registration.next()
    regions = fetch_regions()
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for region in regions:
        inline_kb.add(
            InlineKeyboardButton(region, callback_data=region_callback.new(name=region))
        )
    await message.reply("Please select your region:", reply_markup=inline_kb)


@dp.message_handler(state=Registration.region)
async def process_region_prompt(message: types.Message):
    regions = fetch_regions()
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for region in regions:
        inline_kb.add(
            InlineKeyboardButton(region, callback_data=region_callback.new(name=region))
        )
    await message.reply("Please select your region:", reply_markup=inline_kb)


@dp.callback_query_handler(region_callback.filter(), state=Registration.region)
async def process_region_selection(
    query: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    region = callback_data["name"]
    async with state.proxy() as data:
        data["region"] = region
        data["telegram_id"] = query.from_user.id
        data["telegram_username"] = query.from_user.username
        add_user_to_database(data)
    await state.finish()
    user_data[query.from_user.id] = {"awaiting_question": True}
    await query.message.reply("Region selected: " + region)
    await present_options(query.message)


@dp.message_handler(lambda message: message.text in ["FAQ", "Categories", "Back"])
async def process_query_options(message: types.Message):
    await message.reply(f"You pressed the {message.text} button.")


@dp.callback_query_handler(option_callback.filter(name="Categories"))
async def process_categories_option(query: types.CallbackQuery):
    categories = fetch_categories()
    if not categories:
        await query.answer("No categories found in the database.")
        return
    message_text = "Select a category by its ID:\n"
    inline_kb = InlineKeyboardMarkup(row_width=1)
    for index, category_name in enumerate(categories, start=1):
        category_id_button = InlineKeyboardButton(
            f"{index}. {category_name}", callback_data=f"category_{index}"
        )
        inline_kb.add(category_id_button)
    await query.message.reply(message_text, reply_markup=inline_kb)
    await query.answer()


@dp.callback_query_handler(lambda query: query.data.startswith("category_"))
async def process_category_selection(query: types.CallbackQuery):
    category_index = int(query.data.split("_")[1])
    categories = fetch_categories()
    if 1 <= category_index <= len(categories):
        selected_category = categories[category_index - 1]
        user_telegram_id = query.from_user.id
        user_database_id = get_user_database_id(user_telegram_id)
        if user_database_id is not None:
            await query.message.reply(
                f"You selected category: {selected_category}. Please enter your question."
            )
            user_data[user_telegram_id] = {
                "category_id": category_index,
                "awaiting_question": True,
            }
            print("The cursed function is being called: ", user_data)
        else:
            await query.answer("User not found in the database.")
    else:
        await query.answer("Invalid category selection.")


@dp.message_handler(
    lambda message: user_data.get(message.from_user.id, {}).get("awaiting_question")
)
async def process_user_question(message: types.Message):
    user_telegram_id = message.from_user.id
    user_data_entry = user_data.get(user_telegram_id, {})
    if "category_id" in user_data_entry and "awaiting_question" in user_data_entry:
        category_id = user_data_entry["category_id"]
        user_data_entry.pop("category_id")
        user_data_entry.pop("awaiting_question")
        user_database_id = get_user_database_id(user_telegram_id)
        if user_database_id:
            create_new_question(message.text, False, category_id, user_database_id)
            await message.reply("Your question has been submitted!")
            # Send notification to admin
            admin_message = f"New question submitted:\n{message.text}"
            for admin_id in ADMIN_IDS:
                await bot.send_message(admin_id, admin_message)
        else:
            await message.reply("User not found in the database.")
    else:
        await message.reply("Please select a category first.")


# --------------------------- ADMIN POSSILBE ACTIONS ---------------------------------
@dp.message_handler(commands=["savollar"], user_is_admin=True)
async def view_questions(message: types.Message):
    questions = fetch_unanswered_questions()
    for q_id, text in questions:
        inline_kb = InlineKeyboardMarkup()
        inline_kb.add(InlineKeyboardButton("Answer", callback_data=f"answer_{q_id}"))
        await message.reply(f"Question {q_id}: {text}", reply_markup=inline_kb)


@dp.callback_query_handler(lambda query: query.data.startswith("answer_"))
async def process_answer(query: types.CallbackQuery):
    question_id = query.data.split("_")[1]
    admin_response_state[query.from_user.id] = {
        "awaiting_response": True,
        "question_id": question_id,
    }
    await query.message.reply(f"Iltimos so'rov uchun javobingizni yozing")


@dp.message_handler(lambda message: waiting_for_admin_response_condition(message))
async def save_admin_response(message: types.Message):
    admin_id = message.from_user.id
    response = message.text
    user_data = admin_response_state.get(admin_id)
    if user_data:
        question_id = user_data["question_id"]
        save_answer_to_database(question_id, response, admin_id)
        user_telegram_id = get_user_telegram_id_from_question(question_id)
        question = fetch_question_text(question_id)
        if user_telegram_id:
            await bot.send_message(
                user_telegram_id,
                f"Berilgan savol: {question}\nAdmindan Javob: {response}",
            )
        await message.reply(f"Javob muvaffaqiyatli jonatildi: \n{question_id}.")
        admin_response_state.pop(admin_id)


if __name__ == "__main__":
    executor.start_polling(dp)
