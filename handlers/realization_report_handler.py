from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton

from database.database import database
from request_process.request_process import get_real_rep_data
from unils.utils import get_mounth_depth_of_report
from filters.callback import MonthCallBackFactory, ItemCallBackFactory
from aiogram.utils.keyboard import InlineKeyboardBuilder

real_report_router = Router()


@real_report_router.callback_query(F.data == 'real_rep')
async def get_month_of_rep(callback: CallbackQuery):
    if callback.from_user.id not in database:
        await callback.message.answer(
            text='Вы не ввели данные магазина\n'
                 'пожалуйста заполните недостающие данные\n'
                 '/shop_data',
        )
    else:
        month_list = get_mounth_depth_of_report()
        month_list.pop()
        kb_builder = InlineKeyboardBuilder()
        buttons: list[InlineKeyboardButton] = [
            InlineKeyboardButton(
                text=selected_month,
                callback_data=MonthCallBackFactory(
                    month=selected_month
                ).pack()) for selected_month in month_list
        ]
        kb_builder.row(*buttons, width=3)

        await callback.message.answer(
            text='Выберите месяц за который вы хотите получить отчет month_of_real_rep',
            reply_markup=kb_builder.as_markup()
        )
        await callback.answer()


@real_report_router.callback_query(MonthCallBackFactory.filter())
async def get_real_report_handler(callback: CallbackQuery,
                                  callback_data: MonthCallBackFactory):
    selected_month = callback_data.to_json()
    shop_id = database[callback.from_user.id]['client_id']
    api_key = database[callback.from_user.id]['api_key']
    item_list = [key for key in get_real_rep_data(shop_id, api_key, selected_month)]

    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text=item[:20],
            callback_data=ItemCallBackFactory(
                month=selected_month,
                item=item[:20]
            ).pack()) for item in item_list
    ]
    kb_builder.row(*buttons, width=3)

    await callback.message.answer(
        text='Выберите артикул по которому хотите получить отчет',
        reply_markup=kb_builder.as_markup()
    )
    await callback.answer()



@real_report_router.callback_query(ItemCallBackFactory.filter())
async def get_real_report_handler(callback: CallbackQuery,
                                  callback_data: ItemCallBackFactory):
    product_and_selected_month = callback_data
    shop_id = database[callback.from_user.id]['client_id']
    api_key = database[callback.from_user.id]['api_key']
    data: dict = get_real_rep_data(shop_id, api_key, product_and_selected_month.month)
    product_number = product_and_selected_month.item

    await callback.message.answer(
            text=f'артикул: {product_number}\n'
                 f'продано шт.: {data[product_number]["sale_qty"]}\n'
                 f'продано на сумму: {data[product_number]["sale_price_seller"]:.2f} руб.\n'
                 f'вернули шт.: {data[product_number]["return_qty"]}\n'
                 f'вернули на сумму: {data[product_number]["return_price_seller"]:.2f} руб.\n'
        )
    await callback.answer()
