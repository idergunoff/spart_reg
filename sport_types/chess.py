from config import *


class ChessStates(StatesGroup):
    FULLNAME = State()
    BIRTHDAY = State()
    COMPANY = State()
    POSITION = State()
    PHONE = State()
    END = State()


@dp.message_handler(commands=['cancel'], state='*')
@logger.catch
async def cancel(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await msg.reply('Вы отменили регистрацию')
    logger.info(f'USER "{msg.from_user.id}" COMMAND CANCEL')


@dp.callback_query_handler(text='chess')
@logger.catch
async def wo(call: types.CallbackQuery):
    await ChessStates.FULLNAME.set()
    await call.message.edit_text('<b>Участник</b>\nОтправьте ФИО полностью\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=ChessStates.FULLNAME)
@logger.catch
async def fullname(msg: types.Message, state: FSMContext):
    await state.update_data(fullname=msg.text)
    await ChessStates.BIRTHDAY.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте дату рождения в формате ДД.ММ.ГГГГ'
                                             '\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=ChessStates.BIRTHDAY)
@logger.catch
async def birthday(msg: types.Message, state: FSMContext):
    await state.update_data(birthday=msg.text)
    await ChessStates.COMPANY.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте место работы (наименование '
                                             'подразделения/управление/отдел/служба/цех)\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=ChessStates.COMPANY)
@logger.catch
async def company(msg: types.Message, state: FSMContext):
    await state.update_data(company=msg.text)
    await ChessStates.POSITION.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте должность\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=ChessStates.POSITION)
@logger.catch
async def position(msg: types.Message, state: FSMContext):
    await state.update_data(position=msg.text)
    await ChessStates.PHONE.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте номер телефона\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=ChessStates.PHONE)
@logger.catch
async def phone(msg: types.Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    await ChessStates.END.set()
    chess_data = await state.get_data()
    btn_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
    btn_confirm = InlineKeyboardButton('Подтвердить', callback_data='confirm')
    keyboard = InlineKeyboardMarkup(row_width=2).add(btn_cancel, btn_confirm)
    mes = f'<b>ШАХМАТЫ♟♕</b>\n\n' \
          f'<b><u>Участник</u></b>\n<i><b>ФИО:</b></i> {chess_data["fullname"]}\n<i><b>Дата рождения:</b></i> {chess_data["birthday"]}\n' \
          f'<i><b>Место работы:</b></i> {chess_data["company"]}\n<i><b>Должность:</b></i> {chess_data["position"]}\n<b><i>Телефон:</i></b> {chess_data["phone"]}\n\n' \
          f'<i>Подтвердить? Если в данных допущены ошибки, нажмите на кнопку "Отмена" и повторите регистрацию</i>'
    await bot.send_message(msg.from_user.id, mes, reply_markup=keyboard)


@dp.callback_query_handler(state=ChessStates.END, text='confirm')
@logger.catch
async def confirm(call: types.CallbackQuery, state: FSMContext):
    chess_data = await state.get_data()
    new_person = Person(full_name=chess_data['fullname'], birthday=chess_data['birthday'],
                        company=chess_data['company'], position=chess_data['position'], phone=chess_data['phone'])
    session.add(new_person)
    session.commit()
    new_chess = Chess(username_reg=call.from_user.username, date_reg=datetime.now(), player=new_person.id)
    session.add(new_chess)
    session.commit()
    await call.message.answer('Регистрация участника в турнире по шахматам прошла успешно')
    await state.finish()
    await call.answer()


@dp.callback_query_handler(state=ChessStates.END, text='cancel')
@logger.catch
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Регистрация отменена')
    await call.message.delete()
    await call.answer()

