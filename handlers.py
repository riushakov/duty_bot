from datetime import datetime

import aiogram.enums as enums
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from table import Event
import config
import utils
import logging


router = Router()


@router.message(Command("add"))
async def add_event(msg: Message):
    try:
        message_data = utils.parse_telegram_message(msg)

        chat_id = message_data['chat_id']
        username = message_data['username']
        date = message_data['date']
        text = message_data['text']
        env = message_data['env']
        url = message_data['urls']

        new_pos = Event.new_pos(chat_id=chat_id, date=date)
        status = config.STATUS_WAITING

        Event.add_event(
            chat_id=chat_id,
            username=username,
            date=date,
            text=text,
            env=env,
            pos=new_pos,
            status=status,
            url=url,
            is_active=1
        )

        print_events_message = utils.create_print_message(
            Event.get_all_events(
            chat_id=chat_id,
            date=date,
            status=['processing', 'waiting']
            )
        )

        await msg.answer(
            f"Событие {new_pos} создано\n"
            f"---\n"
            f"{print_events_message}"
        )



    except Exception as e:
        logging.log(level=logging.ERROR, msg=e)
        await msg.answer(
            "Событие не получилось создать"
        )


@router.message(Command("go"))
async def go_event(msg: Message):
    try:
        message_data = utils.parse_telegram_message(msg)

        chat_id = message_data['chat_id']
        dt = datetime.fromtimestamp(message_data['unix_dt'])
        date = message_data['date']
        pos = int(message_data['text'])
        new_status = config.STATUS_PROCESSING

        event = Event.get_event(chat_id=chat_id, date=date, pos=pos)

        event.update_event(
            dt_start=dt,
            status=new_status
        )

        await msg.answer("Ивент запущен")

    except Exception as e:
        logging.log(level=logging.ERROR, msg=e)
        await msg.answer(
            "Ивент не получилось запустить\n"
            "Ожидаем формат /go [event_position]"
        )


@router.message(Command("end"))
async def end_event(msg: Message):
    try:
        message_data = utils.parse_telegram_message(msg)

        chat_id = message_data['chat_id']
        dt = datetime.fromtimestamp(message_data['unix_dt'])
        date = message_data['date']
        pos = int(message_data['text'])
        new_status = config.STATUS_FINISHED

        event = Event.get_event(chat_id=chat_id, date=date, pos=pos)

        event.update_event(
            dt_finish=dt,
            status=new_status
        )

        duration = event.dt_finish - event.dt_start

        await msg.answer(f"Ивент завершен"
                         f"Длительность: {duration}")

    except Exception as e:
        logging.log(level=logging.ERROR, msg=e)
        await msg.answer(
            "Ивент не получилось завершить\n"
            "Ожидаю формат /end [event_position]"
        )


@router.message(Command("cancel"))
async def cancel_event(msg: Message):
    try:
        message_data = utils.parse_telegram_message(msg)

        chat_id = message_data['chat_id']
        dt = None
        date = message_data['date']
        pos = int(message_data['text'])
        new_status = config.STATUS_CANCELLED

        event = Event.get_event(chat_id=chat_id, date=date, pos=pos)

        event.update_event(
            dt_start=dt,
            dt_finish=dt,
            status=new_status
        )

        await msg.answer(f"Ивент отменен ")

    except Exception as e:
        logging.log(level=logging.ERROR, msg=e)
        await msg.answer(
            "Ивент не получилось отменить\n"
            "Ожидаю формат /cancel [event_position]"
        )


@router.message(Command("print"))
async def print_event(msg: Message):
    try:
        message_data = utils.parse_telegram_message(msg)
        text = message_data['text']
        chat_id = message_data['chat_id']
        date = message_data['date']

        events = Event.get_all_events(chat_id=chat_id, date=date, is_active=1)

        message = utils.create_print_message(events)
        await msg.answer(message)

    except Exception as e:
        logging.log(level=logging.ERROR, msg=e)
        await msg.answer(
            "Не получилось вывести"
        )

@router.message(Command("clear"))
async def clear_events(msg: Message):
    try:
        message_data = utils.parse_telegram_message(msg)
        chat_id = message_data['chat_id']
        date = message_data['date']

        events = Event.get_all_events(chat_id=chat_id, date=date, is_active=1)
        for event in events:
            event.update_event(is_active=0)

        await msg.answer("Список очищен")

    except Exception as e:
        logging.log(level=logging.ERROR, msg=e)
        await msg.answer(
            "Не получилось очистить"
        )



@router.message(Command("swap"))
async def swap_events(msg: Message):
    try:
        message_data = utils.parse_telegram_message(msg)
        chat_id = message_data['chat_id']
        date = message_data['date']
        text = message_data['text'].split(' ')

        pos1, pos2 = int(text[0]), int(text[1])
        event1 = Event.get_event(chat_id=chat_id, date=date, pos=pos1)
        event2 = Event.get_event(chat_id=chat_id, date=date, pos=pos2)

        event1.update_event(pos=pos2)
        event2.update_event(pos=pos1)

        await msg.answer('sda')

    except Exception as e:
        logging.log(level=logging.ERROR, msg=e)
        await msg.answer(
            "Не получилось поменять местами\n"
            "Ожидаю формат /swap [event_position] [event_position]"
        )


@router.message(Command("move"))
async def swap_events(msg: Message):
    try:
        message_data = utils.parse_telegram_message(msg)
        chat_id = message_data['chat_id']
        date = message_data['date']
        text = message_data['text'].split(' ')

        pos1, pos2 = int(text[0]), int(text[1])


        await msg.answer('sda')

    except Exception as e:
        logging.log(level=logging.ERROR, msg=e)
        await msg.answer(
            "Не получилось переместить\n"
            "Ожидаю формат /swap [event_position_from] [event_position_to]"
        )


@router.message(Command("event"))
async def link(msg: Message):
    try:
        message_data = utils.parse_telegram_message(msg)
        chat_id = message_data['chat_id']
        date = message_data['date']
        pos = int(message_data['text'])

        event = Event.get_event(chat_id=chat_id, date=date, pos=pos)
        message = utils.create_event_message(event=event)

        await msg.answer(message, parse_mode=enums.ParseMode.HTML)

    except Exception as e:
        logging.log(level=logging.ERROR, msg=e)
        await msg.answer(
            "Не получилось найти событие\n"
            "Ожидаю формат /event [event_position]"
        )
