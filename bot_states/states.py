from aiogram.fsm.state import State, StatesGroup


class GetHeaders(StatesGroup):
    '''Состояние для сохранения HEADER PARAMETERS'''
    shop_id = State()
    api_key = State()
