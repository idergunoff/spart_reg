from config import *

@dp.message_handler(commands=['admin'])
@logger.catch
async def admin(msg: types.Message):
    admin = session.query(Admin).filter(Admin.admin_id == msg.from_user.id).first()
    if not admin:
        new_admin = Admin( admin_id=msg.from_user.id, username=msg.from_user.username, confirm=False)
        session.add(new_admin)
        session.commit()
    else:
        if admin.confirm:
            mes = 'У вас уже есть правa администратора'
        else:
            mes = 'Вы уже отправляли запрос'
        await bot.send_message(msg.from_user.id, mes)
        return
    kb_confirm_admin = InlineKeyboardMarkup(row_width=2)
    btn_yes = InlineKeyboardButton('Да', callback_data=cb_confirm_admin.new(admin_id=msg.from_user.id, confirm='Yes'))
    btn_no = InlineKeyboardButton('Нет', callback_data=cb_confirm_admin.new(admin_id=msg.from_user.id, confirm='No'))
    kb_confirm_admin.add(btn_yes, btn_no)
    for i in super_admin:
        await bot.send_message(i, f'Пользователь <b>"{msg.from_user.username}"</b> подал запрос на предоставление прав '
                                  f'администратора. Предоставить права?', reply_markup=kb_confirm_admin)
    mes = 'Запрос на предоставление прав администратора успешно отправлен'
    await bot.send_message(msg.from_user.id, mes)
    logger.info(f'USER "{msg.from_user.id}" COMMAND ADMIN')


@dp.callback_query_handler(cb_confirm_admin.filter())
@logger.catch
async def confirm_admin(call: types.CallbackQuery, callback_data: dict):
    admin = session.query(Admin).filter(Admin.admin_id == callback_data['admin_id']).first()
    if not admin:
        return
    if callback_data['confirm'] == 'Yes':
        session.query(Admin).filter(Admin.admin_id == admin.admin_id).update({Admin.confirm: True}, synchronize_session='fetch')
        session.commit()
        mes = f'Пользователю <b>"{admin.username}"</b> предоставлены права администратора'
        await bot.send_message(call.from_user.id, mes)
        await bot.send_message(admin.admin_id, 'Вам предоставлены права администратора. Для выгрузки данных отправьте команду /tab')
        logger.info(f'USER "{call.from_user.id}" COMMAND CONFIRM ADMIN')
    else:
        mes = f'Пользователю <b>"{admin.username}"</b>отказано предоставление прав администратора'
        await bot.send_message(call.from_user.id, mes)
        await bot.send_message(admin.admin_id, 'Вам отказано в предоставлении прав администратора')
    await call.answer()


@dp.message_handler(commands=['tab'])
@logger.catch
async def tab(msg: types.Message):
    admin = session.query(Admin).filter(Admin.admin_id == msg.from_user.id, Admin.confirm == True).first()
    if admin or msg.from_user.id in super_admin:
        kb_tab = InlineKeyboardMarkup(row_width=1)
        bv_count = session.query(BeachVolleyball).count()
        btn_bv_tab = InlineKeyboardButton(f'📥Пляжный волейбол🏐🏖️ ({bv_count})', callback_data='bv_tab')
        sb_count = session.query(Streetball).count()
        btn_sb_tab = InlineKeyboardButton(f'📥Стритбол🏀🏙️ ({sb_count})', callback_data='sb_tab')
        wo_count = session.query(Workout).count()
        btn_wo_tab = InlineKeyboardButton(f'📥Воркаут💪🏋 ({wo_count})', callback_data='wo_tab')
        wb_count = session.query(Wakeboarding).count()
        btn_wb_tab = InlineKeyboardButton(f'📥Вейкбординг🏄‍♂️🌊 ({wb_count})', callback_data='wb_tab')
        rc_count = session.query(RockClimbing).count()
        btn_rc_tab = InlineKeyboardButton(f'📥Скалолазание🧗‍♂️🏔️ ({rc_count})', callback_data='rc_tab')
        fcr_count = session.query(FamilyCatamaranRacing).count()
        btn_fcr_tab = InlineKeyboardButton(f'📥Семейные гонки на катамаранах⛵👩‍❤️‍👨 ({fcr_count})', callback_data='fcr_tab')
        ccw_count = session.query(ChildrenClimbingWall).count()
        btn_ccw_tab = InlineKeyboardButton(f'📥Детский скалодром👶🧗‍♂️ ({ccw_count})', callback_data='ccw_tab')
        chess_count = session.query(Chess).count()
        btn_chess_tab = InlineKeyboardButton(f'📥Шахматы♟♕ ({chess_count})', callback_data='chess_tab')
        ff_count = session.query(FigitalFootball).count()
        btn_ff_tab = InlineKeyboardButton(f'📥Фиджитал-футбол🎮⚽ ({ff_count})', callback_data='ff_tab')
        ss_count = session.query(SupSurfing).count()
        btn_ss_tab = InlineKeyboardButton(f'📥SUP серфинг🏄‍♂️🏄‍♀️️ ({ss_count})', callback_data='ss_tab')
        kb_tab.add(btn_bv_tab, btn_sb_tab, btn_wo_tab, btn_wb_tab, btn_rc_tab, btn_fcr_tab, btn_ccw_tab, btn_chess_tab, btn_ff_tab, btn_ss_tab)
        mes = 'Выберите соревнование для выгрузки в таблицу'
        await bot.send_message(msg.from_user.id, mes, reply_markup=kb_tab)
    else:
        mes = 'У вас нет прав администратора'
        await bot.send_message(msg.from_user.id, mes)
        return


@dp.callback_query_handler(text='bv_tab')
@logger.catch
async def bv_tab(call: types.CallbackQuery):
    user = session.query(Admin).filter(Admin.admin_id == call.from_user.id, Admin.confirm == True).first()
    if not user:
        await bot.send_message(call.from_user.id, 'У вас нет прав администратора')
        return
    list_column = ['Номер', 'ФИО', 'Дата рождения', 'Место работы', 'Должность', 'Телефон', 'Дата регистрации', 'Имя пользователя телеграм']
    list_width = [6, 35, 15, 25, 25, 20, 15, 25]
    bd = Side(style='thin', color="000000")
    wb = Workbook()
    ws = wb.active
    for n, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        ws[f'{col}1'] = list_column[n]
        ws.column_dimensions[col].width = list_width[n]
    row = ws.row_dimensions[1]
    row.font = Font(bold=True, name='Calibri', size=10)
    row = ws.row_dimensions[1]
    row.border = Border(bottom=bd)
    n_row = 2
    for n_team, team in enumerate(session.query(BeachVolleyball).all()):
        p1 = session.query(Person).filter(Person.id == team.player_1).first()
        ws[f'A{n_row}'] = n_team + 1
        ws[f'B{n_row}'] = p1.full_name
        ws[f'C{n_row}'] = p1.birthday
        ws[f'D{n_row}'] = p1.company
        ws[f'E{n_row}'] = p1.position
        ws[f'F{n_row}'] = p1.phone
        ws[f'G{n_row}'] = team.date_reg.strftime("%d.%m.%Y")
        ws[f'H{n_row}'] = team.username_reg
        n_row += 1
        p2 = session.query(Person).filter(Person.id == team.player_2).first()
        ws[f'B{n_row}'] = p2.full_name
        ws[f'C{n_row}'] = p2.birthday
        ws[f'D{n_row}'] = p2.company
        ws[f'E{n_row}'] = p2.position
        ws[f'F{n_row}'] = p2.phone
        row = ws.row_dimensions[n_row]
        row.border = Border(bottom=bd)
        n_row += 1
    file_name = 'Пляжный волейбол.xlsx'
    wb.save(file_name)
    await bot.send_document(call.from_user.id, open(file_name, 'rb'))
    os.remove(file_name)



@dp.callback_query_handler(text='sb_tab')
@logger.catch
async def sb_tab(call: types.CallbackQuery):
    user = session.query(Admin).filter(Admin.admin_id == call.from_user.id, Admin.confirm == True).first()
    if not user:
        await bot.send_message(call.from_user.id, 'У вас нет прав администратора')
        return
    list_column = ['Номер', 'ФИО', 'Дата рождения', 'Место работы', 'Должность', 'Телефон', 'Дата регистрации', 'Имя пользователя телеграм']
    list_width = [6, 35, 15, 25, 25, 20, 15, 25]
    bd = Side(style='thin', color="000000")
    wb = Workbook()
    ws = wb.active
    for n, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        ws[f'{col}1'] = list_column[n]
        ws.column_dimensions[col].width = list_width[n]
    row = ws.row_dimensions[1]
    row.font = Font(bold=True, name='Calibri', size=10)
    row = ws.row_dimensions[1]
    row.border = Border(bottom=bd)
    n_row = 2
    for n_team, team in enumerate(session.query(Streetball).all()):
        p1 = session.query(Person).filter(Person.id == team.player_1).first()
        ws[f'A{n_row}'] = n_team + 1
        ws[f'B{n_row}'] = p1.full_name
        ws[f'C{n_row}'] = p1.birthday
        ws[f'D{n_row}'] = p1.company
        ws[f'E{n_row}'] = p1.position
        ws[f'F{n_row}'] = p1.phone
        ws[f'G{n_row}'] = team.date_reg.strftime("%d.%m.%Y")
        ws[f'H{n_row}'] = team.username_reg
        n_row += 1
        p2 = session.query(Person).filter(Person.id == team.player_2).first()
        ws[f'B{n_row}'] = p2.full_name
        ws[f'C{n_row}'] = p2.birthday
        ws[f'D{n_row}'] = p2.company
        ws[f'E{n_row}'] = p2.position
        ws[f'F{n_row}'] = p2.phone
        n_row += 1
        p3 = session.query(Person).filter(Person.id == team.player_3).first()
        ws[f'B{n_row}'] = p3.full_name
        ws[f'C{n_row}'] = p3.birthday
        ws[f'D{n_row}'] = p3.company
        ws[f'E{n_row}'] = p3.position
        ws[f'F{n_row}'] = p3.phone
        n_row += 1
        p4 = session.query(Person).filter(Person.id == team.player_4).first()
        ws[f'B{n_row}'] = p4.full_name
        ws[f'C{n_row}'] = p4.birthday
        ws[f'D{n_row}'] = p4.company
        ws[f'E{n_row}'] = p4.position
        ws[f'F{n_row}'] = p4.phone
        row = ws.row_dimensions[n_row]
        row.border = Border(bottom=bd)
        n_row += 1
    file_name = 'Стритбол.xlsx'
    wb.save(file_name)
    await bot.send_document(call.from_user.id, open(file_name, 'rb'))
    os.remove(file_name)


@dp.callback_query_handler(text='ff_tab')
@logger.catch
async def ff_tab(call: types.CallbackQuery):
    user = session.query(Admin).filter(Admin.admin_id == call.from_user.id, Admin.confirm == True).first()
    if not user:
        await bot.send_message(call.from_user.id, 'У вас нет прав администратора')
        return
    list_column = ['Номер', 'ФИО', 'Дата рождения', 'Место работы', 'Должность', 'Телефон', 'Дата регистрации', 'Имя пользователя телеграм']
    list_width = [6, 35, 15, 25, 25, 20, 15, 25]
    bd = Side(style='thin', color="000000")
    wb = Workbook()
    ws = wb.active
    for n, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        ws[f'{col}1'] = list_column[n]
        ws.column_dimensions[col].width = list_width[n]
    row = ws.row_dimensions[1]
    row.font = Font(bold=True, name='Calibri', size=10)
    row = ws.row_dimensions[1]
    row.border = Border(bottom=bd)
    n_row = 2
    for n_team, team in enumerate(session.query(FigitalFootball).all()):
        p1 = session.query(Person).filter(Person.id == team.player_1).first()
        ws[f'A{n_row}'] = n_team + 1
        ws[f'B{n_row}'] = p1.full_name
        ws[f'C{n_row}'] = p1.birthday
        ws[f'D{n_row}'] = p1.company
        ws[f'E{n_row}'] = p1.position
        ws[f'F{n_row}'] = p1.phone
        ws[f'G{n_row}'] = team.date_reg.strftime("%d.%m.%Y")
        ws[f'H{n_row}'] = team.username_reg
        n_row += 1
        p2 = session.query(Person).filter(Person.id == team.player_2).first()
        ws[f'B{n_row}'] = p2.full_name
        ws[f'C{n_row}'] = p2.birthday
        ws[f'D{n_row}'] = p2.company
        ws[f'E{n_row}'] = p2.position
        ws[f'F{n_row}'] = p2.phone
        n_row += 1
        p3 = session.query(Person).filter(Person.id == team.player_3).first()
        ws[f'B{n_row}'] = p3.full_name
        ws[f'C{n_row}'] = p3.birthday
        ws[f'D{n_row}'] = p3.company
        ws[f'E{n_row}'] = p3.position
        ws[f'F{n_row}'] = p3.phone
        n_row += 1
        p4 = session.query(Person).filter(Person.id == team.player_4).first()
        ws[f'B{n_row}'] = p4.full_name
        ws[f'C{n_row}'] = p4.birthday
        ws[f'D{n_row}'] = p4.company
        ws[f'E{n_row}'] = p4.position
        ws[f'F{n_row}'] = p4.phone
        row = ws.row_dimensions[n_row]
        row.border = Border(bottom=bd)
        n_row += 1
    file_name = 'Фиджитал_футбол.xlsx'
    wb.save(file_name)
    await bot.send_document(call.from_user.id, open(file_name, 'rb'))
    os.remove(file_name)


@dp.callback_query_handler(text='fcr_tab')
@logger.catch
async def fcr_tab(call: types.CallbackQuery):
    user = session.query(Admin).filter(Admin.admin_id == call.from_user.id, Admin.confirm == True).first()
    if not user:
        await bot.send_message(call.from_user.id, 'У вас нет прав администратора')
        return
    list_column = ['Номер', 'ФИО', 'Дата рождения', 'Место работы', 'Должность', 'Телефон', 'Дата регистрации', 'Имя пользователя телеграм']
    list_width = [6, 35, 15, 25, 25, 20, 15, 25]
    bd = Side(style='thin', color="000000")
    wb = Workbook()
    ws = wb.active
    for n, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        ws[f'{col}1'] = list_column[n]
        ws.column_dimensions[col].width = list_width[n]
    row = ws.row_dimensions[1]
    row.font = Font(bold=True, name='Calibri', size=10)
    row = ws.row_dimensions[1]
    row.border = Border(bottom=bd)
    n_row = 2
    for n_team, team in enumerate(session.query(FamilyCatamaranRacing).all()):
        p1 = session.query(Person).filter(Person.id == team.player_1).first()
        ws[f'A{n_row}'] = n_team + 1
        ws[f'B{n_row}'] = p1.full_name
        ws[f'C{n_row}'] = p1.birthday
        ws[f'D{n_row}'] = p1.company
        ws[f'E{n_row}'] = p1.position
        ws[f'F{n_row}'] = p1.phone
        ws[f'G{n_row}'] = team.date_reg.strftime("%d.%m.%Y")
        ws[f'H{n_row}'] = team.username_reg
        n_row += 1
        p2 = session.query(Person).filter(Person.id == team.player_2).first()
        ws[f'B{n_row}'] = p2.full_name
        ws[f'C{n_row}'] = p2.birthday
        ws[f'D{n_row}'] = p2.company
        ws[f'E{n_row}'] = p2.position
        ws[f'F{n_row}'] = p2.phone
        row = ws.row_dimensions[n_row]
        row.border = Border(bottom=bd)
        n_row += 1
    file_name = 'Семейные_гонки_на_катамаранах.xlsx'
    wb.save(file_name)
    await bot.send_document(call.from_user.id, open(file_name, 'rb'))
    os.remove(file_name)


@dp.callback_query_handler(text='wo_tab')
@logger.catch
async def wo_tab(call: types.CallbackQuery):
    user = session.query(Admin).filter(Admin.admin_id == call.from_user.id, Admin.confirm == True).first()
    if not user:
        await bot.send_message(call.from_user.id, 'У вас нет прав администратора')
        return
    list_column = ['Номер', 'ФИО', 'Дата рождения', 'Место работы', 'Должность', 'Телефон', 'Дата регистрации', 'Имя пользователя телеграм']
    list_width = [6, 35, 15, 25, 25, 20, 15, 25]
    bd = Side(style='thin', color="000000")
    wb = Workbook()
    ws = wb.active
    for n, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        ws[f'{col}1'] = list_column[n]
        ws.column_dimensions[col].width = list_width[n]
    row = ws.row_dimensions[1]
    row.font = Font(bold=True, name='Calibri', size=10)
    row = ws.row_dimensions[1]
    row.border = Border(bottom=bd)
    n_row = 2
    for n_team, team in enumerate(session.query(Workout).all()):
        p1 = session.query(Person).filter(Person.id == team.player).first()
        ws[f'A{n_row}'] = n_team + 1
        ws[f'B{n_row}'] = p1.full_name
        ws[f'C{n_row}'] = p1.birthday
        ws[f'D{n_row}'] = p1.company
        ws[f'E{n_row}'] = p1.position
        ws[f'F{n_row}'] = p1.phone
        ws[f'G{n_row}'] = team.date_reg.strftime("%d.%m.%Y")
        ws[f'H{n_row}'] = team.username_reg
        row = ws.row_dimensions[n_row]
        row.border = Border(bottom=bd)
        n_row += 1
    file_name = 'Воркаут.xlsx'
    wb.save(file_name)
    await bot.send_document(call.from_user.id, open(file_name, 'rb'))
    os.remove(file_name)


@dp.callback_query_handler(text='wb_tab')
@logger.catch
async def wb_tab(call: types.CallbackQuery):
    user = session.query(Admin).filter(Admin.admin_id == call.from_user.id, Admin.confirm == True).first()
    if not user:
        await bot.send_message(call.from_user.id, 'У вас нет прав администратора')
        return
    list_column = ['Номер', 'ФИО', 'Дата рождения', 'Место работы', 'Должность', 'Телефон', 'Дата регистрации', 'Имя пользователя телеграм']
    list_width = [6, 35, 15, 25, 25, 20, 15, 25]
    bd = Side(style='thin', color="000000")
    wb = Workbook()
    ws = wb.active
    for n, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        ws[f'{col}1'] = list_column[n]
        ws.column_dimensions[col].width = list_width[n]
    row = ws.row_dimensions[1]
    row.font = Font(bold=True, name='Calibri', size=10)
    row = ws.row_dimensions[1]
    row.border = Border(bottom=bd)
    n_row = 2
    for n_team, team in enumerate(session.query(Wakeboarding).all()):
        p1 = session.query(Person).filter(Person.id == team.player).first()
        ws[f'A{n_row}'] = n_team + 1
        ws[f'B{n_row}'] = p1.full_name
        ws[f'C{n_row}'] = p1.birthday
        ws[f'D{n_row}'] = p1.company
        ws[f'E{n_row}'] = p1.position
        ws[f'F{n_row}'] = p1.phone
        ws[f'G{n_row}'] = team.date_reg.strftime("%d.%m.%Y")
        ws[f'H{n_row}'] = team.username_reg
        row = ws.row_dimensions[n_row]
        row.border = Border(bottom=bd)
        n_row += 1
    file_name = 'Вейкбординг.xlsx'
    wb.save(file_name)
    await bot.send_document(call.from_user.id, open(file_name, 'rb'))
    os.remove(file_name)


@dp.callback_query_handler(text='rc_tab')
@logger.catch
async def rc_tab(call: types.CallbackQuery):
    user = session.query(Admin).filter(Admin.admin_id == call.from_user.id, Admin.confirm == True).first()
    if not user:
        await bot.send_message(call.from_user.id, 'У вас нет прав администратора')
        return
    list_column = ['Номер', 'ФИО', 'Дата рождения', 'Место работы', 'Должность', 'Телефон', 'Дата регистрации', 'Имя пользователя телеграм']
    list_width = [6, 35, 15, 25, 25, 20, 15, 25]
    bd = Side(style='thin', color="000000")
    wb = Workbook()
    ws = wb.active
    for n, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        ws[f'{col}1'] = list_column[n]
        ws.column_dimensions[col].width = list_width[n]
    row = ws.row_dimensions[1]
    row.font = Font(bold=True, name='Calibri', size=10)
    row = ws.row_dimensions[1]
    row.border = Border(bottom=bd)
    n_row = 2
    for n_team, team in enumerate(session.query(RockClimbing).all()):
        p1 = session.query(Person).filter(Person.id == team.player).first()
        ws[f'A{n_row}'] = n_team + 1
        ws[f'B{n_row}'] = p1.full_name
        ws[f'C{n_row}'] = p1.birthday
        ws[f'D{n_row}'] = p1.company
        ws[f'E{n_row}'] = p1.position
        ws[f'F{n_row}'] = p1.phone
        ws[f'G{n_row}'] = team.date_reg.strftime("%d.%m.%Y")
        ws[f'H{n_row}'] = team.username_reg
        row = ws.row_dimensions[n_row]
        row.border = Border(bottom=bd)
        n_row += 1
    file_name = 'Скалолазание.xlsx'
    wb.save(file_name)
    await bot.send_document(call.from_user.id, open(file_name, 'rb'))
    os.remove(file_name)


@dp.callback_query_handler(text='chess_tab')
@logger.catch
async def chess_tab(call: types.CallbackQuery):
    user = session.query(Admin).filter(Admin.admin_id == call.from_user.id, Admin.confirm == True).first()
    if not user:
        await bot.send_message(call.from_user.id, 'У вас нет прав администратора')
        return
    list_column = ['Номер', 'ФИО', 'Дата рождения', 'Место работы', 'Должность', 'Телефон', 'Дата регистрации', 'Имя пользователя телеграм']
    list_width = [6, 35, 15, 25, 25, 20, 15, 25]
    bd = Side(style='thin', color="000000")
    wb = Workbook()
    ws = wb.active
    for n, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        ws[f'{col}1'] = list_column[n]
        ws.column_dimensions[col].width = list_width[n]
    row = ws.row_dimensions[1]
    row.font = Font(bold=True, name='Calibri', size=10)
    row = ws.row_dimensions[1]
    row.border = Border(bottom=bd)
    n_row = 2
    for n_team, team in enumerate(session.query(Chess).all()):
        p1 = session.query(Person).filter(Person.id == team.player).first()
        ws[f'A{n_row}'] = n_team + 1
        ws[f'B{n_row}'] = p1.full_name
        ws[f'C{n_row}'] = p1.birthday
        ws[f'D{n_row}'] = p1.company
        ws[f'E{n_row}'] = p1.position
        ws[f'F{n_row}'] = p1.phone
        ws[f'G{n_row}'] = team.date_reg.strftime("%d.%m.%Y")
        ws[f'H{n_row}'] = team.username_reg
        row = ws.row_dimensions[n_row]
        row.border = Border(bottom=bd)
        n_row += 1
    file_name = 'Шахматы.xlsx'
    wb.save(file_name)
    await bot.send_document(call.from_user.id, open(file_name, 'rb'))
    os.remove(file_name)


@dp.callback_query_handler(text='ss_tab')
@logger.catch
async def ss_tab(call: types.CallbackQuery):
    user = session.query(Admin).filter(Admin.admin_id == call.from_user.id, Admin.confirm == True).first()
    if not user:
        await bot.send_message(call.from_user.id, 'У вас нет прав администратора')
        return
    list_column = ['Номер', 'ФИО', 'Дата рождения', 'Место работы', 'Должность', 'Телефон', 'Дата регистрации', 'Имя пользователя телеграм']
    list_width = [6, 35, 15, 25, 25, 20, 15, 25]
    bd = Side(style='thin', color="000000")
    wb = Workbook()
    ws = wb.active
    for n, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
        ws[f'{col}1'] = list_column[n]
        ws.column_dimensions[col].width = list_width[n]
    row = ws.row_dimensions[1]
    row.font = Font(bold=True, name='Calibri', size=10)
    row = ws.row_dimensions[1]
    row.border = Border(bottom=bd)
    n_row = 2
    for n_team, team in enumerate(session.query(SupSurfing).all()):
        p1 = session.query(Person).filter(Person.id == team.player).first()
        ws[f'A{n_row}'] = n_team + 1
        ws[f'B{n_row}'] = p1.full_name
        ws[f'C{n_row}'] = p1.birthday
        ws[f'D{n_row}'] = p1.company
        ws[f'E{n_row}'] = p1.position
        ws[f'F{n_row}'] = p1.phone
        ws[f'G{n_row}'] = team.date_reg.strftime("%d.%m.%Y")
        ws[f'H{n_row}'] = team.username_reg
        row = ws.row_dimensions[n_row]
        row.border = Border(bottom=bd)
        n_row += 1
    file_name = 'SUPсерфинг.xlsx'
    wb.save(file_name)
    await bot.send_document(call.from_user.id, open(file_name, 'rb'))
    os.remove(file_name)


@dp.callback_query_handler(text='ccw_tab')
@logger.catch
async def ccw_tab(call: types.CallbackQuery):
    user = session.query(Admin).filter(Admin.admin_id == call.from_user.id, Admin.confirm == True).first()
    if not user:
        await bot.send_message(call.from_user.id, 'У вас нет прав администратора')
        return
    list_column = ['Номер', 'ФИО родителя', 'ФИО ребенка', 'Дата рождения', 'Место работы', 'Должность', 'Телефон', 'Дата регистрации', 'Имя пользователя телеграм']
    list_width = [6, 35, 35, 15, 25, 25, 20, 15, 25]
    bd = Side(style='thin', color="000000")
    wb = Workbook()
    ws = wb.active
    for n, col in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']):
        ws[f'{col}1'] = list_column[n]
        ws.column_dimensions[col].width = list_width[n]
    row = ws.row_dimensions[1]
    row.font = Font(bold=True, name='Calibri', size=10)
    row = ws.row_dimensions[1]
    row.border = Border(bottom=bd)
    n_row = 2
    for n_team, team in enumerate(session.query(ChildrenClimbingWall).all()):
        p1 = session.query(Person).filter(Person.id == team.player).first()
        ws[f'A{n_row}'] = n_team + 1
        ws[f'B{n_row}'] = team.parent_name
        ws[f'C{n_row}'] = p1.full_name
        ws[f'D{n_row}'] = p1.birthday
        ws[f'E{n_row}'] = p1.company
        ws[f'F{n_row}'] = p1.position
        ws[f'G{n_row}'] = p1.phone
        ws[f'H{n_row}'] = team.date_reg.strftime("%d.%m.%Y")
        ws[f'I{n_row}'] = team.username_reg
        row = ws.row_dimensions[n_row]
        row.border = Border(bottom=bd)
        n_row += 1
    file_name = 'Детский_скалодром.xlsx'
    wb.save(file_name)
    await bot.send_document(call.from_user.id, open(file_name, 'rb'))
    os.remove(file_name)

