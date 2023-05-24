from contextlib import suppress

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

from bot.keyboard.inline_keyboard import get_keyboard_fab_for_start, get_keyboard_select_procedures, \
    get_keyboard_change_fab_back
from bot.text.about_us import ABOUT_US
from bot.text.start_text import START_TEXT

callback_keyboard = CallbackData("procedures", "action", "value")


async def update_text_fab(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard))


# Хэндлер на команду /start
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    text = START_TEXT['start_text']
    await message.answer(
        text,
        reply_markup=get_keyboard_fab_for_start(callback_keyboard)
    )


async def callbacks_change_fab(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "sign_up":
        await update_text_fab(call.message, 'Отлично! Выберете процедуру:', get_keyboard_select_procedures)
    elif action == "your_recordings":
        await update_text_fab(call.message, 'вы выбрали your_recordings', get_keyboard_fab_for_start)
    elif action == "about_us":
        await update_text_fab(call.message, ABOUT_US[action], get_keyboard_change_fab_back)
    await call.answer()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


# Просто функция, которая доступна только администратору,
# чей ID указан в файле конфигурации.
async def secret_command(message: types.Message):
    await message.answer("Поздравляю! Эта команда доступна только администратору бота.")


def register_handlers_common(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(secret_command, IDFilter(user_id=admin_id), commands="abracadabra")
    dp.register_callback_query_handler(
        callbacks_change_fab,
        callback_keyboard.filter(action=[
            "about_us",
            "your_recordings",
            "sign_up",
        ]
        ))
