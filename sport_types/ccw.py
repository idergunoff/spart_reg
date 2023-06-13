from config import *


class CCWtates(StatesGroup):
    PARENT = State()
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


@dp.callback_query_handler(text='ccw')
@logger.catch
async def wo(call: types.CallbackQuery):
    await CCWtates.PARENT.set()
    await call.message.edit_text('<b>Участник</b>\nОтправьте ФИО родителя ребенка полностью\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=CCWtates.PARENT)
@logger.catch
async def parent(msg: types.Message, state: FSMContext):
    await state.update_data(parent=msg.text)
    await CCWtates.FULLNAME.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте ФИО ребенка полностью\n\n<i>Для отмены нажмите /cancel</i>')



@dp.message_handler(state=CCWtates.FULLNAME)
@logger.catch
async def fullname(msg: types.Message, state: FSMContext):
    await state.update_data(fullname=msg.text)
    await CCWtates.BIRTHDAY.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте дату рождения ребенка в формате ДД.ММ.ГГГГ'
                                             '\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=CCWtates.BIRTHDAY)
@logger.catch
async def birthday(msg: types.Message, state: FSMContext):
    await state.update_data(birthday=msg.text)
    await CCWtates.COMPANY.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте место работы родителя (наименование '
                                             'подразделения/управление/отдел/служба/цех)\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=CCWtates.COMPANY)
@logger.catch
async def company(msg: types.Message, state: FSMContext):
    await state.update_data(company=msg.text)
    await CCWtates.POSITION.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте должность родителя\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=CCWtates.POSITION)
@logger.catch
async def position(msg: types.Message, state: FSMContext):
    await state.update_data(position=msg.text)
    await CCWtates.PHONE.set()
    await bot.send_message(msg.from_user.id, '<b>Участник</b>\nОтправьте номер телефона родителя\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=CCWtates.PHONE)
@logger.catch
async def phone(msg: types.Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    await CCWtates.END.set()
    ccw_data = await state.get_data()
    btn_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
    btn_confirm = InlineKeyboardButton('Подтвердить', callback_data='confirm')
    keyboard = InlineKeyboardMarkup(row_width=2).add(btn_cancel, btn_confirm)
    mes = f'<b>ДЕТСКИЙ СКАЛОДРОМ👶🧗‍♂️</b>\n\n' \
          f'<b><u>Участник</u></b>\n<i><b>ФИО родителя:</b></i> {ccw_data["parent"]}\n<i><b>ФИО ребенка:</b></i> ' \
          f'{ccw_data["fullname"]}\n<i><b>Дата рождения ребенка:</b></i> {ccw_data["birthday"]}\n' \
          f'<i><b>Место работы родителя:</b></i> {ccw_data["company"]}\n<i><b>Должность родителя:</b></i> ' \
          f'{ccw_data["position"]}\n<b><i>Телефон родителя:</i></b> {ccw_data["phone"]}\n\n' \
          f'<i>Подтвердить? Если в данных допущены ошибки, нажмите на кнопку "Отмена" и повторите регистрацию</i>'
    await bot.send_message(msg.from_user.id, mes, reply_markup=keyboard)


@dp.callback_query_handler(state=CCWtates.END, text='confirm')
@logger.catch
async def confirm(call: types.CallbackQuery, state: FSMContext):
    ccw_data = await state.get_data()
    new_person = Person(full_name=ccw_data['fullname'], birthday=ccw_data['birthday'],
                        company=ccw_data['company'], position=ccw_data['position'], phone=ccw_data['phone'])
    session.add(new_person)
    session.commit()
    new_ccw = ChildrenClimbingWall(parent_name=ccw_data['parent'], username_reg=call.from_user.username, date_reg=datetime.now(), player=new_person.id)
    session.add(new_ccw)
    session.commit()
    await call.message.answer('Регистрация участника в соревновании по детскому скалодрому прошла успешно')
    await state.finish()
    await call.answer()


@dp.callback_query_handler(state=CCWtates.END, text='cancel')
@logger.catch
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Регистрация отменена')
    await call.message.delete()
    await call.answer()

