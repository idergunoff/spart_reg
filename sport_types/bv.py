from config import *


class BVStatus(StatesGroup):
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


@dp.callback_query_handler(text='bv')
@logger.catch
async def bv(call: types.CallbackQuery):
    await BVStatus.FULLNAME_1.set()
    await call.message.edit_text('<b>Участник 1 (мужчина)</b>\nОтправьте ФИО полностью\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=BVStatus.FULLNAME_1)
@logger.catch
async def fullname_1(msg: types.Message, state: FSMContext):
    await state.update_data(fullname_1=msg.text)
    await BVStatus.BIRTHDAY_1.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 1 (мужчина)</b>\nОтправьте дату рождения в формате ДД.ММ.ГГГГ'
                                             '\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=BVStatus.BIRTHDAY_1)
@logger.catch
async def birthday_1(msg: types.Message, state: FSMContext):
    await state.update_data(birthday_1=msg.text)
    await BVStatus.COMPANY_1.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 1 (мужчина)</b>\nОтправьте место работы (наименование '
                                             'подразделения/управление/отдел/служба/цех)\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=BVStatus.COMPANY_1)
@logger.catch
async def company_1(msg: types.Message, state: FSMContext):
    await state.update_data(company_1=msg.text)
    await BVStatus.POSITION_1.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 1 (мужчина)</b>\nОтправьте должность\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=BVStatus.POSITION_1)
@logger.catch
async def position_1(msg: types.Message, state: FSMContext):
    await state.update_data(position_1=msg.text)
    await BVStatus.PHONE_1.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 1 (мужчина)</b>\nОтправьте номер телефона\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=BVStatus.PHONE_1)
@logger.catch
async def phone_1(msg: types.Message, state: FSMContext):
    await state.update_data(phone_1=msg.text)
    await BVStatus.FULLNAME_2.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 2 (женщина)</b>\nОтправьте ФИО полностью\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=BVStatus.FULLNAME_2)
@logger.catch
async def fullname_2(msg: types.Message, state: FSMContext):
    await state.update_data(fullname_2=msg.text)
    await BVStatus.BIRTHDAY_2.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 2 (женщина)</b>\nОтправьте дату рождения в формате ДД.ММ.ГГГГ'
                                             '\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=BVStatus.BIRTHDAY_2)
@logger.catch
async def birthday_2(msg: types.Message, state: FSMContext):
    await state.update_data(birthday_2=msg.text)
    await BVStatus.COMPANY_2.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 2 (женщина)</b>\nОтправьте место работы (наименование '
                                             'подразделения/управление/отдел/служба/цех)\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=BVStatus.COMPANY_2)
@logger.catch
async def company_2(msg: types.Message, state: FSMContext):
    await state.update_data(company_2=msg.text)
    await BVStatus.POSITION_2.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 2 (женщина)</b>\nОтправьте должность\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=BVStatus.POSITION_2)
@logger.catch
async def position_2(msg: types.Message, state: FSMContext):
    await state.update_data(position_2=msg.text)
    await BVStatus.PHONE_2.set()
    await bot.send_message(msg.from_user.id, '<b>Участник 2 (женщина)</b>\nОтправьте номер телефона\n\n<i>Для отмены нажмите /cancel</i>')


@dp.message_handler(state=BVStatus.PHONE_2)
@logger.catch
async def phone_2(msg: types.Message, state: FSMContext):
    await state.update_data(phone_2=msg.text)
    await BVStatus.END.set()
    bv_data = await state.get_data()
    btn_cancel = InlineKeyboardButton('Отмена', callback_data='cancel')
    btn_confirm = InlineKeyboardButton('Подтвердить', callback_data='confirm')
    keyboard = InlineKeyboardMarkup(row_width=2).add(btn_cancel, btn_confirm)
    mes = f'<b>ПЛЯЖНЫЙ ВОЛЕЙБОЛ🏐🏖️</b>\n\n' \
          f'<b><u>Участник 1 (мужчина)</u></b>\n<i><b>ФИО:</b></i> {bv_data["fullname_1"]}\n<i><b>Дата рождения:</b></i> {bv_data["birthday_1"]}\n' \
          f'<i><b>Место работы:</b></i> {bv_data["company_1"]}\n<i><b>Должность:</b></i> {bv_data["position_1"]}\n<b><i>Телефон:</i></b> {bv_data["phone_1"]}\n' \
          f'<b><u>Участник 2 (женщина)</u></b>\n<i><b>ФИО:</b></i> {bv_data["fullname_2"]}\n<i><b>Дата рождения:</b></i> {bv_data["birthday_2"]}\n' \
          f'<i><b>Место работы:</b></i> {bv_data["company_2"]}\n<i><b>Должность:</b></i> {bv_data["position_2"]}\n<i><b>Телефон:</b></i> {bv_data["phone_2"]}\n\n' \
          f'<i>Подтвердить? Если в данных допущены ошибки, нажмите на кнопку "Отмена" и повторите регистрацию</i>'
    await bot.send_message(msg.from_user.id, mes, reply_markup=keyboard)


@dp.callback_query_handler(state=BVStatus.END, text='confirm')
@logger.catch
async def confirm(call: types.CallbackQuery, state: FSMContext):
    bv_data = await state.get_data()
    new_person_1 = Person(full_name=bv_data['fullname_1'], birthday=bv_data['birthday_1'],
                        company=bv_data['company_1'], position=bv_data['position_1'], phone=bv_data['phone_1'])
    new_person_2 = Person(full_name=bv_data['fullname_2'], birthday=bv_data['birthday_2'],
                        company=bv_data['company_2'], position=bv_data['position_2'], phone=bv_data['phone_2'])
    session.add(new_person_1)
    session.add(new_person_2)
    session.commit()
    new_bv = BeachVolleyball(username_reg=call.from_user.username, date_reg=datetime.now(), player_1=new_person_1.id,
                             player_2=new_person_2.id)
    session.add(new_bv)
    session.commit()
    await call.message.answer('Регистрация команды по пляжным волейболу прошла успешно')
    await state.finish()
    await call.answer()


@dp.callback_query_handler(state=BVStatus.END, text='cancel')
@logger.catch
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer('Регистрация отменена')
    await call.message.delete()
    await call.answer()

