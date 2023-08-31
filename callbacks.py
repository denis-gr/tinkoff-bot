from aiogram.filters.callback_data import CallbackData

class MarkCallbackFactory(CallbackData, prefix="mark"):
    action: str
    mes_id: int

class ReportCallbackFactory(CallbackData, prefix="report"):
    action: str
    mes_id: int
    is_harmful: bool = False
    is_lie: bool = False
    is_useless: bool = False
    is_back: bool = False
    is_comment: bool = False
