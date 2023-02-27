import logging
import os
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверяет доступность переменных окружения."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID and ENDPOINT:
        return True
    else:
        logging.critical(
            'Отсутствует одна или несколько переменных окружения.')
        return False


def send_message(bot, message):
    """Отправляет сообщение пользователю."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as error:
        logging.error(f'Ошибка отправки сообщения: {error}')
        raise exceptions.MessageSendingError(
            f'Сообщение {message} не было отправлено. Смотри журнал ошибок.')
    logging.debug(f'Сообщение "{message}" отправлено.')


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    payload = {'from_date': timestamp}
    massage = 'Ошибка при запросе к API. Смотри журнал ошибок.'
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
    except Exception as error:
        logging.error(f'Эндпоинт API не доступен: {error}')
        raise exceptions.EndpointAnswerException(massage)
    if response.status_code != HTTPStatus.OK:
        logging.error(f'Код ответа API: {response.status_code}')
        raise exceptions.EndpointAnswerException(massage)
    try:
        return response.json()
    except Exception as error:
        logging.error(f'Ошибка преобразования к формату json: {error}')
        raise exceptions.EndpointAnswerException(massage)


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    message = 'Ошибка ответа от API. Смотри журнал ошибок.'
    if type(response) != dict:
        logging.error('Тип данных в ответе API не является словарем.')
        raise TypeError(message)
    if 'homeworks' not in response:
        logging.error('Ключ homeworks отсутствует в словаре.')
        raise exceptions.CheckResponseException(message)
    homeworks_list = response['homeworks']
    if type(homeworks_list) != list:
        logging.error(
            'Тип данных значения по ключу homeworks не является списком.')
        raise TypeError(message)
    return homeworks_list


def parse_status(homework):
    """Извлекает статус домашней работы."""
    message = 'Ошибка получения статуса домашней работы. Смотри журнал ошибок.'
    if 'homework_name' not in homework:
        logging.error('Ключ homework_name недоступен')
        raise KeyError(message)
    if 'status' not in homework:
        logging.error('Ключ status недоступен')
        raise KeyError(message)
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if homework_status in HOMEWORK_VERDICTS:
        verdict = HOMEWORK_VERDICTS[homework_status]
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    else:
        logging.error(
            f'Передан неожиданный статус домашней работы "{homework_status}"')
        raise exceptions.ParseStatusException(message)


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        raise exceptions.GlobalsError(
            'Ошибка глобальной переменной. Смотри журнал ошибок.')

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    current_status = ''
    current_error = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            homework = check_response(response)
            if not len(homework):
                logging.debug('Статус не обновлен')
                send_message(bot, 'Статус не обновлен')
            else:
                homework_status = parse_status(homework[0])
                if current_status == homework_status:
                    logging.debug(homework_status)
                else:
                    current_status = homework_status
                    send_message(bot, homework_status)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            if current_error != str(error):
                current_error = str(error)
                send_message(bot, message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s, %(name)s, %(levelname)s, %(message)s, %(lineno)s',
        level=logging.DEBUG,
        filename='Info.log',
        filemode='w'
    )
    main()
