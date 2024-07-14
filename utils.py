from aiogram.types import Message, MessageEntity
import config
from datetime import datetime as dt
from urllib.parse import urlparse
from table import Event


def parse_telegram_message(message: Message):
    text = message.text.split()
    command = text[0]
    env = config.ENV_PROD
    username = '@' + message.from_user.username
    unix_dt = int(dt.now().timestamp())
    urls_list = [entity.url for entity in [entities for entities in [mes_entities for mes_entities in message.entities]]
            if entity.url]  # Список гиперссылок
    if len(urls_list) == 0:
        urls = []
    else:
        urls = urls_list


    for word in text:
        if word in config.ENV_TEST_WORDS:
            env = config.ENV_TEST
        elif '@' in word:
            username = word
        elif ('https://' or 'http://') in word:
            urls.append(word)

    message_data = {
        'message_id': message.message_id,
        'date': message.date.date(),
        'unix_dt': unix_dt,
        'username': username,
        'chat_id': message.chat.id,
        'text': message.text.replace(command + ' ', ''),
        'env': env,
        'urls': str(urls)
    }

    return message_data


def create_print_message(events: Event):
    message = ''
    if len(events) != 0:
        message += f''  # Список работ на проде {dt.date(dt.today())}:\n\n
        for event in events:
            message += (f"{config.SMILE_STATUS[event.status]} "
                        f"{event.pos}.  "
                        f"{event.text} "
                        f"{event.username}\n")
    else:
        message = 'На сегодня работ еще не запланировано'
    return message


def create_event_message(event: Event):
    message = (
        f'Событие {event.pos}:\n'
        f'Дата: {event.date}\n'
        f'Статус: {event.status}\n'
        f'Исполнитель: {event.username}\n'
        f'Текст: {event.text}\n'
        f'Дата начала: {event.dt_start}\n'
        f'Дата завершения: {event.dt_finish}\n'
        f'Среда: {event.env}\n'
        f'Ссылки: {create_links(event.url)}\n'

    )
    return message


def create_links(string_of_urls):
    links = ''
    if string_of_urls != None:
        cleaned_string = string_of_urls.strip("[]").replace("'", "")
        # cleaned_string = string_of_urls.strip("[]")
        list_of_urls = cleaned_string.split(", ")

        for url in list_of_urls:
            domain = urlparse(url).netloc.split('.')

            if domain[0] != 'www':
                text = domain[0]
            else:
                text = domain[1]

            if text in config.SERVICE_NAME:
                hyperlink = f'<a href="{url}">{config.SERVICE_NAME[text]}</a>'
            else:
                hyperlink = f'<a href="{url}">{text}</a>'

            links += hyperlink + '  '
    else:
        list_of_urls = []
        links = 'Не указано'


    return links



