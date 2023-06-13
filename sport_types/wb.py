from config import *


class WBStates(StatesGroup):
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


@dp.callback_query_handler(text='wb')
@logger.catch
async def wo(call: types.CallbackQuery):
    await WBStates.FULLNAME.set()
    await call.message.edit_text('<b>Участник</b>\nОтправьте ФИО полностью\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=WBStates.FULLNAME)
@logger.catch
async def fullname(msg: types.Message, state: FSMContext):
    await state.update_data(fullname=msg.text)
    await WBStates.BIRTHDAY.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте дату рождения в формате ДД.ММ.ГГГГ'
                                             '\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=WBStates.BIRTHDAY)
@logger.catch
async def birthday(msg: types.Message, state: FSMContext):
    await state.update_data(birthday=msg.text)
    await WBStates.COMPANY.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте место работы (наименование '
                                             'подразделения/управление/отдел/служба/цех)\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=WBStates.COMPANY)
@logger.catch
async def company(msg: types.Message, state: FSMContext):
    await state.update_data(company=msg.text)
    await WBStates.POSITION.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте должность\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=WBStates.POSITION)
@logger.catch
async def position(msg: types.Message, state: FSMContext):
    await state.update_data(position=msg.text)
    await WBStates.PHONE.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте номер телефона\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=WBStates.PHONE)
@logger.catch
async def phone(msg: types.Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    await WBStates.END.set()
    wb_data = await state.get_data()
    btn_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
    btn_confirm = InlineKeyboardButton('Подтвердить', callback_data='confirm')
    keyboard = InlineKeyboardMarkup(row_width=2).add(btn_cancel, btn_confirm)
    mes = f'<b>ВЕЙКБОРДИНГ🏄‍♂️🌊</b>\n\n' \
          f'<b><u>Участник</u></b>\n<i><b>ФИО:</b></i> {wb_data["fullname"]}\n<i><b>Дата рождения:</b></i> {wb_data["birthday"]}\n' \
          f'<i><b>Место работы:</b></i> {wb_data["company"]}\n<i><b>Должность:</b></i> {wb_data["position"]}\n<b><i>Телефон:</i></b> {wb_data["phone"]}\n\n' \
          f'<i>Подтвердить? Если в данных допущены ошибки, нажмите на кнопку "Отмена" и повторите регистрацию</i>'
    await bot.send_message(msg.from_user.id, mes, reply_markup=keyboard)


@dp.callback_query_handler(state=WBStates.END, text='confirm')
@logger.catch
async def confirm(call: types.CallbackQuery, state: FSMContext):
    wb_data = await state.get_data()
    new_person = Person(full_name=wb_data['fullname'], birthday=wb_data['birthday'],
                        company=wb_data['company'], position=wb_data['position'], phone=wb_data['phone'])
    session.add(new_person)
    session.commit()
    new_wo = Wakeboarding(username_reg=call.from_user.username, date_reg=datetime.now(), player=new_person.id)
    session.add(new_wo)
    session.commit()
    await call.message.answer('Регистрация участника в соревновании по вейкбордингу прошла успешно')
    await state.finish()
    await call.answer()


@dp.callback_query_handler(state=WBStates.END, text='cancel')
@logger.catch
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Регистрация отменена')
    await call.message.delete()
    await call.answer()

