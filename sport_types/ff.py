from config import *


class FFStates(StatesGroup):
    FULLNAME_1 = State()
    BIRTHDAY_1 = State()
    COMPANY_1 = State()
    POSITION_1 = State()
    PHONE_1 = State()
    FULLNAME_2 = State()
    BIRTHDAY_2 = State()
    COMPANY_2 = State()
    POSITION_2 = State()
    PHONE_2 = State()
    FULLNAME_3 = State()
    BIRTHDAY_3 = State()
    COMPANY_3 = State()
    POSITION_3 = State()
    PHONE_3 = State()
    FULLNAME_4 = State()
    BIRTHDAY_4 = State()
    COMPANY_4 = State()
    POSITION_4 = State()
    PHONE_4 = State()
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


@dp.callback_query_handler(text='ff')
@logger.catch
async def bv(call: types.CallbackQuery):
    await FFStates.FULLNAME_1.set()
    await call.message.edit_text('<b>Участник 1</b>\nОтправьте ФИО полностью\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.FULLNAME_1)
@logger.catch
async def fullname_1(msg: types.Message, state: FSMContext):
    await state.update_data(fullname_1=msg.text)
    await FFStates.BIRTHDAY_1.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 1</b>\nОтправьте дату рождения в формате ДД.ММ.ГГГГ'
                                             '\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.BIRTHDAY_1)
@logger.catch
async def birthday_1(msg: types.Message, state: FSMContext):
    await state.update_data(birthday_1=msg.text)
    await FFStates.COMPANY_1.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 1</b>\nОтправьте место работы (наименование '
                                             'подразделения/управление/отдел/служба/цех)\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.COMPANY_1)
@logger.catch
async def company_1(msg: types.Message, state: FSMContext):
    await state.update_data(company_1=msg.text)
    await FFStates.POSITION_1.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 1</b>\nОтправьте должность\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.POSITION_1)
@logger.catch
async def position_1(msg: types.Message, state: FSMContext):
    await state.update_data(position_1=msg.text)
    await FFStates.PHONE_1.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 1</b>\nОтправьте номер телефона\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.PHONE_1)
@logger.catch
async def phone_1(msg: types.Message, state: FSMContext):
    await state.update_data(phone_1=msg.text)
    await FFStates.FULLNAME_2.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 2</b>\nОтправьте ФИО полностью\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.FULLNAME_2)
@logger.catch
async def fullname_2(msg: types.Message, state: FSMContext):
    await state.update_data(fullname_2=msg.text)
    await FFStates.BIRTHDAY_2.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 2</b>\nОтправьте дату рождения в формате ДД.ММ.ГГГГ'
                                             '\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.BIRTHDAY_2)
@logger.catch
async def birthday_2(msg: types.Message, state: FSMContext):
    await state.update_data(birthday_2=msg.text)
    await FFStates.COMPANY_2.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 2</b>\nОтправьте место работы (наименование '
                                             'подразделения/управление/отдел/служба/цех)\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.COMPANY_2)
@logger.catch
async def company_2(msg: types.Message, state: FSMContext):
    await state.update_data(company_2=msg.text)
    await FFStates.POSITION_2.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 2</b>\nОтправьте должность\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.POSITION_2)
@logger.catch
async def position_2(msg: types.Message, state: FSMContext):
    await state.update_data(position_2=msg.text)
    await FFStates.PHONE_2.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 2</b>\nОтправьте номер телефона\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.PHONE_2)
@logger.catch
async def phone_2(msg: types.Message, state: FSMContext):
    await state.update_data(phone_2=msg.text)
    await FFStates.FULLNAME_3.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 3</b>\nОтправьте ФИО полностью\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.FULLNAME_3)
@logger.catch
async def fullname_3(msg: types.Message, state: FSMContext):
    await state.update_data(fullname_3=msg.text)
    await FFStates.BIRTHDAY_3.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 3</b>\nОтправьте дату рождения в формате ДД.ММ.ГГГГ'
                                             '\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.BIRTHDAY_3)
@logger.catch
async def birthday_3(msg: types.Message, state: FSMContext):
    await state.update_data(birthday_3=msg.text)
    await FFStates.COMPANY_3.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 3</b>\nОтправьте место работы (наименование '
                                             'подразделения/управление/отдел/служба/цех)\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.COMPANY_3)
@logger.catch
async def company_3(msg: types.Message, state: FSMContext):
    await state.update_data(company_3=msg.text)
    await FFStates.POSITION_3.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 3</b>\nОтправьте должность\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.POSITION_3)
@logger.catch
async def position_3(msg: types.Message, state: FSMContext):
    await state.update_data(position_3=msg.text)
    await FFStates.PHONE_3.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 3</b>\nОтправьте номер телефона\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.PHONE_3)
@logger.catch
async def phone_3(msg: types.Message, state: FSMContext):
    await state.update_data(phone_3=msg.text)
    await FFStates.FULLNAME_4.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 4</b>\nОтправьте ФИО полностью\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.FULLNAME_4)
@logger.catch
async def fullname_4(msg: types.Message, state: FSMContext):
    await state.update_data(fullname_4=msg.text)
    await FFStates.BIRTHDAY_4.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 4</b>\nОтправьте дату рождения в формате ДД.ММ.ГГГГ'
                                             '\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.BIRTHDAY_4)
@logger.catch
async def birthday_4(msg: types.Message, state: FSMContext):
    await state.update_data(birthday_4=msg.text)
    await FFStates.COMPANY_4.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 4</b>\nОтправьте место работы (наименование '
                                             'подразделения/управление/отдел/служба/цех)\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.COMPANY_4)
@logger.catch
async def company_4(msg: types.Message, state: FSMContext):
    await state.update_data(company_4=msg.text)
    await FFStates.POSITION_4.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 4</b>\nОтправьте должность\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.POSITION_4)
@logger.catch
async def position_4(msg: types.Message, state: FSMContext):
    await state.update_data(position_4=msg.text)
    await FFStates.PHONE_4.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 4</b>\nОтправьте номер телефона\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=FFStates.PHONE_4)
@logger.catch
async def phone_4(msg: types.Message, state: FSMContext):
    await state.update_data(phone_4=msg.text)
    await FFStates.END.set()
    ff_data = await state.get_data()
    btn_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
    btn_confirm = InlineKeyboardButton('Подтвердить', callback_data='confirm')
    keyboard = InlineKeyboardMarkup(row_width=2).add(btn_cancel, btn_confirm)
    mes = f'<b>ФИДЖИТАЛ-ФУТБОЛ🎮⚽</b>\n\n' \
          f'<b><u>Участник 1</u></b>\n<i><b>ФИО:</b></i> {ff_data["fullname_1"]}\n<i><b>Дата рождения:</b></i> {ff_data["birthday_1"]}\n' \
          f'<i><b>Место работы:</b></i> {ff_data["company_1"]}\n<i><b>Должность:</b></i> {ff_data["position_1"]}\n<b><i>Телефон:</i></b> {ff_data["phone_1"]}\n' \
          f'<b><u>Участник 2</u></b>\n<i><b>ФИО:</b></i> {ff_data["fullname_2"]}\n<i><b>Дата рождения:</b></i> {ff_data["birthday_2"]}\n' \
          f'<i><b>Место работы:</b></i> {ff_data["company_2"]}\n<i><b>Должность:</b></i> {ff_data["position_2"]}\n<i><b>Телефон:</b></i> {ff_data["phone_2"]}\n' \
          f'<b><u>Участник 3</u></b>\n<i><b>ФИО:</b></i> {ff_data["fullname_3"]}\n<i><b>Дата рождения:</b></i> {ff_data["birthday_3"]}\n' \
          f'<i><b>Место работы:</b></i> {ff_data["company_3"]}\n<i><b>Должность:</b></i> {ff_data["position_3"]}\n<b><i>Телефон:</i></b> {ff_data["phone_3"]}\n' \
          f'<b><u>Участник 4</u></b>\n<i><b>ФИО:</b></i> {ff_data["fullname_4"]}\n<i><b>Дата рождения:</b></i> {ff_data["birthday_4"]}\n' \
          f'<i><b>Место работы:</b></i> {ff_data["company_4"]}\n<i><b>Должность:</b></i> {ff_data["position_4"]}\n<i><b>Телефон:</b></i> {ff_data["phone_4"]}\n\n' \
          f'<i>Подтвердить? Если в данных допущены ошибки, нажмите на кнопку "Отмена" и повторите регистрацию</i>'
    await bot.send_message(msg.from_user.id, mes, reply_markup=keyboard)


@dp.callback_query_handler(state=FFStates.END, text='confirm')
@logger.catch
async def confirm(call: types.CallbackQuery, state: FSMContext):
    ff_data = await state.get_data()
    new_person_1 = Person(full_name=ff_data['fullname_1'], birthday=ff_data['birthday_1'],
                          company=ff_data['company_1'], position=ff_data['position_1'], phone=ff_data['phone_1'])
    new_person_2 = Person(full_name=ff_data['fullname_2'], birthday=ff_data['birthday_2'],
                          company=ff_data['company_2'], position=ff_data['position_2'], phone=ff_data['phone_2'])
    new_person_3 = Person(full_name=ff_data['fullname_3'], birthday=ff_data['birthday_3'],
                          company=ff_data['company_3'], position=ff_data['position_3'], phone=ff_data['phone_3'])
    new_person_4 = Person(full_name=ff_data['fullname_4'], birthday=ff_data['birthday_4'],
                          company=ff_data['company_4'], position=ff_data['position_4'], phone=ff_data['phone_4'])
    session.add(new_person_1)
    session.add(new_person_2)
    session.add(new_person_3)
    session.add(new_person_4)
    session.commit()
    new_ff = FigitalFootball(username_reg=call.from_user.username, date_reg=datetime.now(), player_1=new_person_1.id,
                        player_2=new_person_2.id, player_3=new_person_3.id, player_4=new_person_4.id)
    session.add(new_ff)
    session.commit()
    await call.message.answer('Регистрация команды по фиджитал-футболу прошла успешно')
    await state.finish()
    await call.answer()


@dp.callback_query_handler(state=FFStates.END, text='cancel')
@logger.catch
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Регистрация отменена')
    await call.message.delete()
    await call.answer()
