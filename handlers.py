from contextlib import suppress

from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram import flags

from keyboards import get_mark_keyboard, get_report_keyboard
from callbacks import MarkCallbackFactory, ReportCallbackFactory
from states import ReportStatesGroup

dp = Router()
dp.message.middleware(ChatActionMiddleware())

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, Юля! Я рада быть здесь, чтобы помочь абитуриентам и студентам ГУАП (Государственный университет аэрокосмического приборостроения в Санкт-Петербурге). Чем я могу помочь тебе сегодня?")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("I help you")


@dp.callback_query(MarkCallbackFactory.filter())
async def mark(callback, callback_data, model):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(callback.message.text,
            reply_markup=get_report_keyboard(action=callback_data.action,
                                             mes_id=callback_data.mes_id))
    await model.report(callback.from_user.id, callback_data.mes_id,
            callback_data.action == "like")
    await callback.answer()


@dp.callback_query(ReportCallbackFactory.filter())
async def report(callback, callback_data, state, model):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(callback.message.text, reply_markup=None)
    await callback.answer()
    if callback_data.is_comment:
        await state.clear()
        await state.set_state(ReportStatesGroup.text)
        await state.set_data({ "callback_data": callback_data })
    else:
        await model.report(callback.from_user.id, callback_data.mes_id,
            callback_data.action == "like", callback_data.is_harmful,
            callback_data.is_lie, callback_data.is_useless)


@dp.message(ReportStatesGroup.text)
async def game_get_help(message, state, model):
    callback_data = (await state.get_data())["callback_data"]
    await model.report(message.from_user.id, callback_data.mes_id,
        callback_data.action == "like", callback_data.is_harmful,
        callback_data.is_lie, callback_data.is_useless, comment=message.text)
    await message.answer(text="Спасибо за коментарий")
    await state.clear()


@dp.message(Command("clear_context"))
@flags.chat_action("typing")
async def cmd_clear_context(message: types.Message, model):
    await model.clear_context(message.from_user.id, message.message_id)


@dp.message(Command("get_metrics"))
@flags.chat_action("typing")
async def cmd_metrics(message: types.Message, model):
    metrics = await model.get_metrics()
    await message.answer("\n".join(f"{k}: {v}" for k, v in metrics.items()))


@dp.message()
@flags.chat_action("typing")
async def cmd_start(message: types.Message, model):
    try:
        answer = await model.ask(message.from_user.id, message.message_id,
            message.text)
        await message.answer(answer, reply_markup=get_mark_keyboard(message.message_id))
    except:
        await message.answer("Ошибка, попробуйте ещё раз поздее")

