from admin import *
from config import *
from sport_types.bv import *
from sport_types.sb import *
from sport_types.wo import *
from sport_types.wb import *
from sport_types.rc import *
from sport_types.fcr import *
from sport_types.ccw import *
from sport_types.chess import *
from sport_types.ff import *
from sport_types.ss import *





@dp.message_handler(commands=['start'])
@logger.catch
async def start(msg: types.Message):
    mes = f'👋\n{msg.from_user.username}, добро пожаловать в бот регистрации участников в  в VII Спартакиаде среди ' \
          f'молодых работников предприятий Группы «Татнефть» и сервисного блока'
    await bot.send_message(msg.from_user.id, mes, reply_markup=kb_start)
    logger.info(f'USER "{msg.from_user.id}" COMMAND START')


@dp.message_handler(text='Регистрация📝')
@logger.catch
async def reg(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Выберите соревнование', reply_markup=kb_types)
    logger.info(f'USER "{msg.from_user.id}" COMMAND REG')


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
