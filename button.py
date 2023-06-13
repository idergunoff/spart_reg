from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from emoji import emojize


# CallbackData


cb_admins = CallbackData('admins', 'chat_id') # id чата для меню админов
cb_add_admin = CallbackData('add_admin', 'chat_id') # id чата для добавления администратора
cb_del_admin = CallbackData('del_admin', 'chat_id') # id чата для удаления администратора
cb_add_user_admin = CallbackData('add_user_admin', 'chat_id', 'user_id') # id чата и юзера для добавления администратора
cb_del_user_admin = CallbackData('del_user_admin', 'chat_id', 'user_id') # id чата и юзера для удаления администратора
cb_back_admins = CallbackData('back_admins', 'chat_id') # id чата для возврата в меню админов
cb_back_task_admin = CallbackData('back_task_admin', 'chat_id') # id чата для выхода из меню админа

cb_update_chat = CallbackData('update_chat', 'chat_id') # id чата и название для обновления chat_id
cb_exit_chat= CallbackData('exit_chat', 'chat_id')  # id чата для выхода из чата


# KeyboardButton

btn_help = KeyboardButton('Помощь🆘')
btn_reg = KeyboardButton('Регистрация📝')


# InlineKeyboardButton

btn_bv = InlineKeyboardButton('Пляжный волейбол🏐🏖️', callback_data='bv')
btn_sb = InlineKeyboardButton('Стритбол🏀🏙️', callback_data='sb')
btn_wo = InlineKeyboardButton('Воркаут💪🏋', callback_data='wo')
btn_wb = InlineKeyboardButton('Вейкбординг🏄‍♂️🌊', callback_data='wb')
btn_rc = InlineKeyboardButton('Скалолазание🧗‍♂️🏔️', callback_data='rc')
btn_fcr = InlineKeyboardButton('Семейные гонки на катамаранах⛵👩‍❤️‍👨', callback_data='fcr')
btn_ccw = InlineKeyboardButton('Детский скалодром👶🧗‍♂️', callback_data='ccw')
btn_chess = InlineKeyboardButton('Шахматы♟♕', callback_data='chess')
btn_ff = InlineKeyboardButton('Фиджитал-футбол🎮⚽', callback_data='ff')
btn_ss = InlineKeyboardButton('SUP серфинг🏄‍♂️🏄‍♀️️', callback_data='ss')


kb_types = InlineKeyboardMarkup(row_width=1)
kb_types.add(btn_bv, btn_sb, btn_wo, btn_wb, btn_rc, btn_fcr, btn_ccw, btn_chess, btn_ff, btn_ss)

# ReplyKeyboardMarkup

kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
kb_start.row(btn_reg, btn_help)


class TaskStates(StatesGroup):
    TIME_TASK = State()
    USER_DELETE = State()



