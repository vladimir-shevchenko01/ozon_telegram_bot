from aiogram.filters.callback_data import CallbackData


class MonthCallBackFactory(CallbackData, prefix='month', sep=':'):
    month: str

    def to_json(self):
        return self.month


class ItemCallBackFactory(CallbackData, prefix='item', sep=':'):
    item: str
    month: str

    def to_json(self):
        return self.item
