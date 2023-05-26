import datetime

from aiogram import types

# from django.utils.timezone import localtime


# localtime()

SET_DATE = []
for my_day in range(0, 7):
    SET_DATE.append(
        (datetime.datetime.now() + datetime.timedelta(days=my_day)).strftime("%m.%d")
    )
PROCEDURES = [
    "Мейкап",
    "Покраска волос",
    "Маникюр",
]

SET_TIME = [
    "10_00", "10_30", "11_00", "11_30",
    "12_00", "12_30", "13_00", "13_30",
    "14_00", "14_30", "15_00", "15_30",
    "16_00", "16_30", "17_00", "17_30",
    "18_00", "18_30", "19_00", "19_30",
    "20_00", "20_30"
]

specialist = ['Ольга', 'Татьяна']


def get_keyboard_choose_specialist(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text=f"✅ Мастер {specialist[0]}",
                                   callback_data=callback_keyboard.new(action="personal_data", value=specialist[0])),
        types.InlineKeyboardButton(text=f"✅ Мастер {specialist[1]}",
                                   callback_data=callback_keyboard.new(action="personal_data", value=specialist[1])),

        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_choose_specialist_before_change_date(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text=f"✅ Мастер {specialist[0]}",
                                   callback_data=callback_keyboard.new(action="select_date", value=specialist[0])),
        types.InlineKeyboardButton(text=f"✅ Мастер {specialist[1]}",
                                   callback_data=callback_keyboard.new(action="select_date", value=specialist[1])),

        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_change_fab_back(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="🔙 Вернутся назад",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_none(callback_keyboard):
    buttons = []
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_fab_for_start(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="Записаться к нам",
                                   callback_data=callback_keyboard.new(action="sign_up", value="")),
        types.InlineKeyboardButton(text="Посмотреть свои записи",
                                   callback_data=callback_keyboard.new(action="your_recordings", value="")),
        types.InlineKeyboardButton(text="О нас",
                                   callback_data=callback_keyboard.new(action="about_us", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_select_procedures(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="Мейкап",
                                   callback_data=callback_keyboard.new(action="make_up", value="")),
        types.InlineKeyboardButton(text="Покраска волос",
                                   callback_data=callback_keyboard.new(action="hair_coloring", value="")),
        types.InlineKeyboardButton(text="Маникюр",
                                   callback_data=callback_keyboard.new(action="manicure", value="")),
        types.InlineKeyboardButton(text="🔙 Вернутся назад",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_sign_up(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(
            text="Записаться на удобное время",
            callback_data=callback_keyboard.new(action="select_date", value="")),
        types.InlineKeyboardButton(text="💁‍♀️Выбрать мастера",
                                   callback_data=callback_keyboard.new(
                                       action="choose_specialist_before_change_date", value="")),
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_select_date(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(
            text="🔚 В начало", callback_data=callback_keyboard.new(action="back", value="")),
        types.InlineKeyboardButton(
            text="🔙 Выбрать процедуру",
            callback_data=callback_keyboard.new(action="back_to_select_procedures", value="")),
    ]
    for my_date in SET_DATE:
        buttons.append(types.InlineKeyboardButton(
            text=f"{my_date}", callback_data=callback_keyboard.new(action="make_an_appointment", value=my_date)))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_make_an_appointment(callback_keyboard):
    buttons = []
    for my_time in SET_TIME:
        buttons.append(types.InlineKeyboardButton(
            text=f"{my_time}",
            callback_data=callback_keyboard.new(action="choose_specialist", value=my_time)))
    buttons.append(types.InlineKeyboardButton(text="🔚 В начало",
                                              callback_data=callback_keyboard.new(action="back", value="")))
    buttons.append(types.InlineKeyboardButton(text="🔙 Изменить день",
                                              callback_data=callback_keyboard.new(
                                                  action="back_to_select_date", value="")))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_appointment_have_choose_specialist(callback_keyboard):
    buttons = []
    for my_time in SET_TIME:
        buttons.append(types.InlineKeyboardButton(
            text=f"{my_time}",
            callback_data=callback_keyboard.new(action="personal_data", value=my_time)))
    buttons.append(types.InlineKeyboardButton(text="🔚 В начало",
                                              callback_data=callback_keyboard.new(action="back", value="")))
    buttons.append(types.InlineKeyboardButton(text="🔙 Изменить день",
                                              callback_data=callback_keyboard.new(
                                                  action="back_to_select_date", value="")))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_personal_data(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="✅ Согласен на обработку ПД",
                                   callback_data=callback_keyboard.new(action="specify_name", value="")),
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value=""))
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard
