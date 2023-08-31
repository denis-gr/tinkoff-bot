from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks import MarkCallbackFactory, ReportCallbackFactory

def get_mark_keyboard(mes_id):
    builder =  InlineKeyboardBuilder()
    builder.button(
        text="👍", callback_data=MarkCallbackFactory(
            action="like", mes_id=mes_id)
    )
    builder.button(
        text="👎", callback_data=MarkCallbackFactory(
            action="dislike", mes_id=mes_id)
    )
    return builder.as_markup()


def get_report_keyboard(action, mes_id):
    builder =  InlineKeyboardBuilder()
    builder.button(
        text="Назад", callback_data=ReportCallbackFactory(
            action=action, mes_id=mes_id, is_back=True)
    )
    builder.button(
        text="Прокоментировать", callback_data=ReportCallbackFactory(
            action=action, mes_id=mes_id, is_comment=True)
    )
    if action == "dislike":
        builder.button(
            text="Это оскорбительно", callback_data=ReportCallbackFactory(
                action=action, mes_id=mes_id, is_harmful=True)
        )
        builder.button(
            text="Это ложь", callback_data=ReportCallbackFactory(
                action=action, mes_id=mes_id, is_lie=True)
        )
        builder.button(
            text="Это бесполезно", callback_data=ReportCallbackFactory(
                action=action, mes_id=mes_id, is_useless=True)
        )
        builder.adjust(2)
    return builder.as_markup()
