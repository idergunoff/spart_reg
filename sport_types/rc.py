from config import *


class RCStates(StatesGroup):
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


@dp.callback_query_handler(text='rc')
@logger.catch
async def wo(call: types.CallbackQuery):
    await RCStates.FULLNAME.set()
    await call.message.edit_text('<b>Участник</b>\nОтправьте ФИО полностью\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=RCStates.FULLNAME)
@logger.catch
async def fullname(msg: types.Message, state: FSMContext):
    await state.update_data(fullname=msg.text)
    await RCStates.BIRTHDAY.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте дату рождения в формате ДД.ММ.ГГГГ'
                                             '\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=RCStates.BIRTHDAY)
@logger.catch
async def birthday(msg: types.Message, state: FSMContext):
    await state.update_data(birthday=msg.text)
    await RCStates.COMPANY.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте место работы (наименование '
                                             'подразделения/управление/отдел/служба/цех)\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=RCStates.COMPANY)
@logger.catch
async def company(msg: types.Message, state: FSMContext):
    await state.update_data(company=msg.text)
    await RCStates.POSITION.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте должность\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=RCStates.POSITION)
@logger.catch
async def position(msg: types.Message, state: FSMContext):
    await state.update_data(position=msg.text)
    await RCStates.PHONE.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте номер телефона\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=RCStates.PHONE)
@logger.catch
async def phone(msg: types.Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    await RCStates.END.set()
    rc_data = await state.get_data()
    btn_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
    btn_confirm = InlineKeyboardButton('Подтвердить', callback_data='confirm')
    keyboard = InlineKeyboardMarkup(row_width=2).add(btn_cancel, btn_confirm)
    mes = f'<b>СКАЛОЛАЗАНИЕ🧗‍♂️🏔️</b>\n\n' \
          f'<b><u>Участник</u></b>\n<i><b>ФИО:</b></i> {rc_data["fullname"]}\n<i><b>Дата рождения:</b></i> {rc_data["birthday"]}\n' \
          f'<i><b>Место работы:</b></i> {rc_data["company"]}\n<i><b>Должность:</b></i> {rc_data["position"]}\n<b><i>Телефон:</i></b> {rc_data["phone"]}\n\n' \
          f'<i>Подтвердить? Если в данных допущены ошибки, нажмите на кнопку "Отмена" и повторите регистрацию</i>'
    await bot.send_message(msg.from_user.id, mes, reply_markup=keyboard)


@dp.callback_query_handler(state=RCStates.END, text='confirm')
@logger.catch
async def confirm(call: types.CallbackQuery, state: FSMContext):
    rc_data = await state.get_data()
    new_person = Person(full_name=rc_data['fullname'], birthday=rc_data['birthday'],
                        company=rc_data['company'], position=rc_data['position'], phone=rc_data['phone'])
    session.add(new_person)
    session.commit()
    new_rc = RockClimbing(username_reg=call.from_user.username, date_reg=datetime.now(), player=new_person.id)
    session.add(new_rc)
    session.commit()
    await call.message.answer('Регистрация участника в соревновании по скалолазанию прошла успешно')
    await state.finish()
    await call.answer()


@dp.callback_query_handler(state=RCStates.END, text='cancel')
@logger.catch
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Регистрация отменена')
    await call.message.delete()
    await call.answer()

