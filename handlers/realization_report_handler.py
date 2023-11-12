from aiogram import Router, F
from aiogram.types import (CallbackQuery,
    Message, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.filters import Command
from request_process.request_process import get_real_rep_data
from database.database import database

real_report_router = Router()


@real_report_router.callback_query(F.data == 'real_rep')
async def get_real_report_handler(callback: CallbackQuery):
    shop_id = database[callback.from_user.id]['client_id']
    api_key = database[callback.from_user.id]['api_key']
    data = get_real_rep_data(shop_id, api_key)
    for item, volume in data.items():
        sale_qty = volume['sale_qty']
        sale_summ = volume['sale_price_seller']
        return_qty = volume['return_qty']
        return_summ = volume['return_price_seller']
        await callback.message.answer(text=f'артикул: {item}\n'
                                   f'продано шт.: {sale_qty}\n'
                                   f'продано на сумму: {sale_summ:.2f} руб.\n'
                                   f'вернули шт.: {return_qty}\n'
                                   f'вернули на сумму: {return_summ:.2f} руб.\n'
        )