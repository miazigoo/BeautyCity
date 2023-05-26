from contextlib import suppress

from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.keyboard.inline_keyboard import *
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from bot.text.start_text import START_TEXT

callback_keyboard = CallbackData("procedures", "action", "value")
USERS_DATA = {}


class PersonalData(StatesGroup):
    waiting_for_get_name = State()
    waiting_for_get_phone = State()


async def update_text_fab(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard))


async def callbacks_change_procedures(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "make_up":
        USERS_DATA['procedures'] = "Мейкап"
        await update_text_fab(call.message,
                              '💄 Процедура "Мейкап" стоит от 900 Руб.', get_keyboard_sign_up)
    elif action == "hair_coloring":
        USERS_DATA['procedures'] = "Покраска волос"
        await update_text_fab(call.message,
                              '🧑🏻‍🎤 Процедура "Покраска волос" стоит от 1200 Руб.', get_keyboard_sign_up)
    elif action == "manicure":
        USERS_DATA['procedures'] = "Маникюр"
        await update_text_fab(call.message,
                              '💅🏼 Процедура "Маникюр" стоит от 1000 Руб.', get_keyboard_sign_up)
    elif action == "back":
        await update_text_fab(call.message, START_TEXT['start_text'], get_keyboard_fab_for_start)
    await call.answer()


async def callbacks_change_date_time(
        call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    action = callback_data["action"]
    print('callback_data', callback_data)
    if action == "select_date":
        USERS_DATA['specialist'] = callback_data["value"]
        await update_text_fab(call.message,
                              '📅 Выберете удобный для вас день:', get_keyboard_select_date)
    elif action == "back_to_select_procedures":
        await update_text_fab(call.message, "Выберете процедуру:", get_keyboard_select_procedures)

    elif action == "choose_specialist":
        change_time = callback_data["value"].split("_")
        hour = change_time[0]
        minuts = change_time[1]
        USERS_DATA['time'] = f"{hour}:{minuts}"
        await update_text_fab(call.message, "Выберете Мастера:", get_keyboard_choose_specialist)

    elif action == "choose_specialist_before_change_date":
        await update_text_fab(call.message, "Выберете Мастера:", get_keyboard_choose_specialist_before_change_date)

    elif action == "make_an_appointment":
        change_date = callback_data["value"]
        USERS_DATA['date'] = change_date
        if not USERS_DATA.get('specialist'):
            await update_text_fab(call.message,
                                  '📅 Выберете удобное время:', get_keyboard_make_an_appointment)
        else:
            await update_text_fab(call.message,
                                  '📅 Выберете удобное время:', get_keyboard_appointment_have_choose_specialist)

    elif action == "back_to_select_date":
        await update_text_fab(call.message, "📅 Выберете удобный для вас день:", get_keyboard_select_date)
    elif action == "personal_data":
        if not USERS_DATA.get('time'):
            change_time = callback_data["value"].split("_")
            hour = change_time[0]
            minuts = change_time[1]
            USERS_DATA['time'] = f"{hour}:{minuts}"
        if not USERS_DATA.get('specialist'):
            USERS_DATA['specialist'] = callback_data["value"]
        text = "Для продолжения записи нам понадобятся ваше Имя и номер телефона. " \
               "Продолжая вы даете согласие на обработку персональных данных"
        await update_text_fab(call.message, text, get_keyboard_personal_data)
    elif action == "specify_name":
        text = "Введите ваше имя: "
        await update_text_fab(call.message, text, get_keyboard_none)
        await state.set_state(PersonalData.waiting_for_get_name.state)
    await call.answer()


async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(chosen_name=message.text)

    await state.set_state(PersonalData.waiting_for_get_phone.state)
    await message.answer("Теперь введите номер телефона в формате\n79995553388 :")


async def get_phone(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data['chosen_name']
    phone = message.text
    USERS_DATA['name'] = name
    USERS_DATA['phone'] = phone
    date_of_admission = USERS_DATA['date']
    time_of_admission = USERS_DATA['time']
    procedures = USERS_DATA.get('procedures')
    master = USERS_DATA.get('specialist')
    await message.answer(
        f"Спасибо за запись {name}! До встречи {date_of_admission} {time_of_admission}\n"
        f"На процедуре {procedures}, у Мастера: {master}"
        f"По адресу: ул. улица д. дом"
    )
    await state.finish()


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
            "personal_data",
            "specify_name",
            "choose_specialist",
            "choose_specialist_before_change_date",
        ]))
    dp.register_message_handler(get_name, state=PersonalData.waiting_for_get_name)
    dp.register_message_handler(get_phone, state=PersonalData.waiting_for_get_phone)
