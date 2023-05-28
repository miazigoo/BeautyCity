from contextlib import suppress

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from asgiref.sync import sync_to_async

from bot.keyboard.inline_keyboard import get_keyboard_fab_for_start
from bot.models import StartText

from bot.text.start_text import START_TEXT

callback_keyboard = CallbackData("procedures", "action", "value")


async def update_text_fab(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard))


@sync_to_async()
def get_start_text():
    about_us = StartText.objects.filter(pk=1)
    if about_us:
        text = about_us[0].descriptions
    else:
        text = START_TEXT['start_text']

    return text


# Хэндлер на команду /start
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    text = await get_start_text()
    await message.answer(
        text,
        reply_markup=get_keyboard_fab_for_start(callback_keyboard)
    )


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
