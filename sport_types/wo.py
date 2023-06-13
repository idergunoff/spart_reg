from config import *


class WOStates(StatesGroup):
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


@dp.callback_query_handler(text='wo')
@logger.catch
async def wo(call: types.CallbackQuery):
    await WOStates.FULLNAME.set()
    await call.message.edit_text('<b>Участник</b>\nОтправьте ФИО полностью\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=WOStates.FULLNAME)
@logger.catch
async def fullname(msg: types.Message, state: FSMContext):
    await state.update_data(fullname=msg.text)
    await WOStates.BIRTHDAY.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте дату рождения в формате ДД.ММ.ГГГГ'
                                             '\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=WOStates.BIRTHDAY)
@logger.catch
async def birthday(msg: types.Message, state: FSMContext):
    await state.update_data(birthday=msg.text)
    await WOStates.COMPANY.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте место работы (наименование '
                                             'подразделения/управление/отдел/служба/цех)\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=WOStates.COMPANY)
@logger.catch
async def company(msg: types.Message, state: FSMContext):
    await state.update_data(company=msg.text)
    await WOStates.POSITION.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте должность\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=WOStates.POSITION)
@logger.catch
async def position(msg: types.Message, state: FSMContext):
    await state.update_data(position=msg.text)
    await WOStates.PHONE.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте номер телефона\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=WOStates.PHONE)
@logger.catch
async def phone(msg: types.Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    await WOStates.END.set()
    wo_data = await state.get_data()
    btn_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
    btn_confirm = InlineKeyboardButton('Подтвердить', callback_data='confirm')
    keyboard = InlineKeyboardMarkup(row_width=2).add(btn_cancel, btn_confirm)
    mes = f'<b>ВОРКАУТ️🏋💪</b>\n\n' \
          f'<b><u>Участник</u></b>\n<i><b>ФИО:</b></i> {wo_data["fullname"]}\n<i><b>Дата рождения:</b></i> {wo_data["birthday"]}\n' \
          f'<i><b>Место работы:</b></i> {wo_data["company"]}\n<i><b>Должность:</b></i> {wo_data["position"]}\n<b><i>Телефон:</i></b> {wo_data["phone"]}\n\n' \
          f'<i>Подтвердить? Если в данных допущены ошибки, нажмите на кнопку "Отмена" и повторите регистрацию</i>'
    await bot.send_message(msg.from_user.id, mes, reply_markup=keyboard)


@dp.callback_query_handler(state=WOStates.END, text='confirm')
@logger.catch
async def confirm(call: types.CallbackQuery, state: FSMContext):
    wo_data = await state.get_data()
    new_person = Person(full_name=wo_data['fullname'], birthday=wo_data['birthday'],
                          company=wo_data['company'], position=wo_data['position'], phone=wo_data['phone'])
    session.add(new_person)
    session.commit()
    new_wo = Workout(username_reg=call.from_user.username, date_reg=datetime.now(), player=new_person.id)
    session.add(new_wo)
    session.commit()
    await call.message.answer('Регистрация участника в соревновании по воркауту прошла успешно')
    await state.finish()
    await call.answer()


@dp.callback_query_handler(state=WOStates.END, text='cancel')
@logger.catch
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Регистрация отменена')
    await call.message.delete()
    await call.answer()

