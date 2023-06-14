from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from emoji import emojize


# CallbackData


cb_confirm_admin = CallbackData('admins', 'admin_id', 'confirm')


# KeyboardButton

btn_info = KeyboardButton('Информацияℹ️')
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
kb_start.row(btn_reg, btn_info)





