import os
from contextlib import suppress
from bot.models import Weekend, Salons, Appointments, Employee, Procedures

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from bot.keyboard.inline_keyboard import *
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from bot.text.start_text import START_TEXT
from asgiref.sync import sync_to_async
from bot.text.about_us import ABOUT_US
# from channels.db import database_sync_to_async
from django.utils.timezone import localtime

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

callback_keyboard = CallbackData("procedures", "action", "value")
today = datetime.datetime.today()
# weekend = sync_to_async(Weekend.objects.all())
USERS_DATA = {}
DATE = {}


# @sync_to_async(thread_sensitive=True)
# def get_all_weekends(date):
#     for weekend in Weekend.objects.filter(not_work_date=date.date()):
#         not_work_date = weekend.not_work_date
#         master = weekend.employee
#         return not_work_date, master


class PersonalData(StatesGroup):
    waiting_for_get_name = State()
    waiting_for_get_phone = State()


async def update_text_fab(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard))


async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(chosen_name=message.text)

    await state.set_state(PersonalData.waiting_for_get_phone.state)
    await message.answer("Теперь введите номер телефона в формате\n79995553388 :")


async def get_phone(message: types.Message, state: FSMContext):
    telegram_id = message.from_id
    print('telegram_id', telegram_id)
    user_data = await state.get_data()
    name = user_data['chosen_name']
    phone = message.text
    USERS_DATA['name'] = name
    USERS_DATA['phone'] = phone
    date_of_admission = USERS_DATA['date']
    time_of_admission = USERS_DATA['time']
    procedures_data = USERS_DATA.get('procedures')
    master_data = USERS_DATA.get('specialist')
    adress = ''
    salon = None
    async for procedures in Procedures.objects.filter(name=procedures_data):
        procedures_data = procedures
    async for master in Employee.objects.filter(name=master_data):
        master_data = master
    async for salon in Salons.objects.filter(pk=1):
        adress = salon.address
        salon = salon
    await Appointments.objects.acreate(
        telegram_id=telegram_id,
        name=USERS_DATA['name'],
        phone_number=phone,
        salon=salon,
        appointment_date=date_of_admission,
        appointment_time=time_of_admission,
        procedure=procedures_data,
        master=master_data
    )
    await message.answer(
        f"Спасибо за запись {name}! До встречи {date_of_admission} {time_of_admission}\n"
        f"На процедуре {procedures}, у Мастера: {master_data}\n"
        f"{adress}"
    )
    await state.finish()


# @sync_to_async
# def get_recordings(user_id):
#     recordings = Appointments.objects.filter(telegram_id=user_id)[:10]
#     return recordings


def get_keyboard_recordings(callback_keyboard):
    user_id = USERS_DATA.get('user_id')
    recordings = Appointments.objects.filter(telegram_id=user_id)[:10]
    buttons = []
    for recording in recordings:
        text = f'{recording.procedure.name}_{recording.appointment_date.strftime("%m-%d")}_{recording.appointment_time}'
        buttons.append(
            types.InlineKeyboardButton(text=f"{text}",
                                       callback_data=callback_keyboard.new(action="to_recordings", value='')),
        )
    buttons.append(types.InlineKeyboardButton(text="🔚 В начало",
                                              callback_data=callback_keyboard.new(action="back", value="")))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def callbacks_change_fab(call: types.CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    USERS_DATA['user_id'] = user_id
    action = callback_data["action"]
    if action == "sign_up":
        USERS_DATA.clear()
        await update_text_fab(call.message, 'Отлично! Выберете процедуру:', get_keyboard_select_procedures)
    elif action == "your_recordings":
        await update_text_fab(call.message, '📝 Ваши записи в нашем Сервисе: ', get_keyboard_recordings)
    elif action == "about_us":
        await update_text_fab(call.message, ABOUT_US[action], get_keyboard_change_fab_back)
    await call.answer()


async def callbacks_change_procedures(call: types.CallbackQuery, callback_data: dict):
    value = callback_data["value"]
    procedure = Procedures.objects.get(pk=int(value))
    USERS_DATA['procedures'] = procedure.name
    await update_text_fab(call.message,
                    f'Процедура "{procedure.name}" стоит от {procedure.price} руб.', get_keyboard_sign_up)
    await call.answer()


async def callbacks_back(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "back":
        USERS_DATA.clear()
        await update_text_fab(call.message, START_TEXT['start_text'], get_keyboard_fab_for_start)
    await call.answer()


def get_keyboard_exclude_specialist(callback_keyboard):
    employee = USERS_DATA.get('employee')
    buttons = []
    for master in Employee.objects.exclude(name=employee):
        buttons.append(
            types.InlineKeyboardButton(text=f"✅ Мастер {master.name}",
                                       callback_data=callback_keyboard.new(action="personal_data",
                                                                           value=master.name)),
        )
    buttons.append(
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


async def callbacks_change_date_time(
        call: types.CallbackQuery, callback_data: dict, state: FSMContext,
):
    action = callback_data["action"]
    if action == "back_to_select_procedures":
        await update_text_fab(call.message, "Выберете процедуру:", get_keyboard_select_procedures)

    elif action == "choose_specialist":
        change_time = callback_data["value"].split("_")
        hour = change_time[0]
        minuts = change_time[1]
        USERS_DATA['time'] = f"{hour}:{minuts}"
        date = USERS_DATA['date']
        not_work_date = USERS_DATA['not_work_date']
        employee = USERS_DATA['employee']
        if not_work_date == date:
            async for master in Employee.objects.exclude(name=employee):
                master_data = master
                print(master_data)

            text = f"У Мастера: {employee} - выходной. Выберете Мастера:"
            await update_text_fab(call.message, text, get_keyboard_exclude_specialist)
        else:
            await update_text_fab(call.message, "Выберете Мастера:", get_keyboard_choose_specialist)

    elif action == "choose_specialist_before_change_date":
        await update_text_fab(call.message, "Выберете Мастера:", get_keyboard_choose_specialist_before_change_date)

    elif action == "back_to_select_date":
        await call.message.edit_text("📅 Выберете удобный для вас день: back_to_select_date",
                                     reply_markup=await SimpleCalendar().start_calendar())
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


async def nav_cal_handler(callback: types.CallbackQuery, callback_data: dict):
    action = callback_data['action']
    if action == 'navigation_calendar':
        if not USERS_DATA.get('specialist'):
            USERS_DATA['specialist'] = callback_data["value"]
            await callback.message.edit_text("📅 Выберете удобный для вас день: navigation_calendar",
                                             reply_markup=await SimpleCalendar().start_calendar())
        else:
            print('callback_data["value"]', callback_data["value"])
            # USERS_DATA['specialist'] = callback_data["value"]
            await callback.message.edit_text(
                "📅 Выберете удобный для вас день: await SimpleCalendar().start_calendar()",
                reply_markup=await SimpleCalendar().start_calendar())
    await callback.answer()


async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        w = []
        async for weekend in Weekend.objects.filter(not_work_date=date.date()):
            w.append(weekend)
        print('w == ', w)
        try:
            not_work_date = w[0].not_work_date or None
            employee = str(w[0].employee) or None
        except IndexError:
            not_work_date = None
            employee = None
        USERS_DATA['date'] = date.date()
        USERS_DATA['not_work_date'] = not_work_date
        USERS_DATA['employee'] = employee
        print('USERS_DATA[date]', USERS_DATA['date'], '\n', USERS_DATA)
        if date.date() < today.date():
            text = "🙅‍♀️Нельзя вернуться в прошлое.\n" \
                   "💃️Но мы можем шагнуть в будущее.\n📅 Выберете удобный для вас день:"
            await callback_query.message.edit_text(text,
                                                   reply_markup=await SimpleCalendar().start_calendar())
        else:
            if not_work_date == date.date() and employee == USERS_DATA.get('specialist'):
                text = f"У мастера {USERS_DATA.get('specialist')} в этот день выходной.\n" \
                       "📅 Выберете другой удобный для вас день или другого мастера:"
                await update_text_fab(callback_query.message,
                                      text, get_keyboard_navigation_calendar)
                print('not_work_date', not_work_date, 'and', date.date())
            elif USERS_DATA.get('specialist'):
                await update_text_fab(callback_query.message,
                                      '📅 Выберете удобное время!!!:',
                                      get_keyboard_appointment_have_choose_specialist)
            elif not USERS_DATA.get('specialist'):
                await update_text_fab(callback_query.message,
                                      '📅 Выберете удобное время: else', get_keyboard_make_an_appointment)

    await callback_query.answer()


def register_handlers_procedures(dp: Dispatcher):
    dp.register_callback_query_handler(
        nav_cal_handler,
        callback_keyboard.filter(action=[
            "navigation_calendar",
        ]))

    dp.register_callback_query_handler(
        callbacks_back,
        callback_keyboard.filter(action=[
            "back",
        ]))

    dp.register_callback_query_handler(
        callbacks_change_procedures,
        callback_keyboard.filter(action=[
            "procedure",
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
            "navigation_calendar",
        ]))

    dp.register_message_handler(get_name, state=PersonalData.waiting_for_get_name)
    dp.register_message_handler(get_phone, state=PersonalData.waiting_for_get_phone)

    dp.register_callback_query_handler(
        process_simple_calendar,
        simple_cal_callback.filter()
    )

    dp.register_callback_query_handler(
        callbacks_change_fab,
        callback_keyboard.filter(action=[
            "about_us",
            "your_recordings",
            "sign_up",
        ]
        ))
