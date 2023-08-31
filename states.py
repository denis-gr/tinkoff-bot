from aiogram.fsm.state import StatesGroup, State

class ReportStatesGroup(StatesGroup):
    text = State()
    callback_data = State()
