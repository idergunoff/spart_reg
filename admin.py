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





