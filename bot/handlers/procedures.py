from contextlib import suppress
from bot.keyboard.inline_keyboard import *
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from bot.text.start_text import START_TEXT

callback_keyboard = CallbackData("procedures", "action", "value")
USERS_DATA = {}


async def update_text_fab(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard))


async def callbacks_change_procedures(call: types.CallbackQuery, callback_data: dict):
    print(callback_data)
    action = callback_data["action"]
    # print(action)
    if action == "make_up":
        USERS_DATA[action] = "Мейкап"
        await update_text_fab(call.message,
                              'Отлично! Процедура "Мейкап" стоит от 900 Руб.', get_keyboard_sign_up)
    elif action == "hair_coloring":
        USERS_DATA[action] = "Покраска волос"
        await update_text_fab(call.message,
                              'Отлично! Процедура "Покраска волос" стоит от 1200 Руб.', get_keyboard_sign_up)
    elif action == "manicure":
        USERS_DATA[action] = "Маникюр"
        await update_text_fab(call.message,
                              'Отлично! Процедура "Маникюр" стоит от 1000 Руб.', get_keyboard_sign_up)
    elif action == "back":
        await update_text_fab(call.message, START_TEXT['start_text'], get_keyboard_fab_for_start)
    await call.answer()


async def callbacks_change_date_time(call: types.CallbackQuery, callback_data: dict):
    # print(callback_data)
    action = callback_data["action"]
    # print(action)
    if action == "select_date":
        await update_text_fab(call.message,
                              'Отлично! Выберете удобную для вас дату:', get_keyboard_select_date)
    elif action == "back_to_select_procedures":
        await update_text_fab(call.message, "Выберете процедуру:", get_keyboard_select_procedures)

    elif action == "make_an_appointment":
        await update_text_fab(call.message,
                              'Отлично! Выберете удобное время:', get_keyboard_make_an_appointment)

    elif action == "back_to_select_date":
        await update_text_fab(call.message, "Выберете удобную для вас дату:", get_keyboard_select_procedures)
    await call.answer()


def register_handlers_procedures(dp: Dispatcher):
    dp.register_callback_query_handler(
        callbacks_change_procedures,
        callback_keyboard.filter(action=[
            "make_up",
            "hair_coloring",
            "manicure",
            "back",
        ]))
    dp.register_callback_query_handler(
        callbacks_change_date_time,
        callback_keyboard.filter(action=[
            "select_date",
            "make_an_appointment",
            "back_to_select_procedures",
            "back_to_select_date",
        ]))
