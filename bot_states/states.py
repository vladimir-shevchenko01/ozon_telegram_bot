from aiogram.fsm.state import State, StatesGroup


class FSMShopHeaders(StatesGroup):
    '''Состояния для получения данных магазина.'''
    shop_id = State()
    api_key = State()


class FSMFinReal(StatesGroup):
    date = State()
