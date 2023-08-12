# homework_bot
# Проект homework_bot

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)

## Описание

Проект "homework_bot" выполняет следующие операции:
* Опрашивает API сервиса Практикум.Домашка с заданным интервалом и проверяет статус отправленной на ревью домашней работы.
* При обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram.
* Логирует свою работу и сообщает о важных проблемах сообщением в Telegram.

## Как запустить проект локально:

Клонировать репозиторий и перейти в него в командной строке:

``` git@github.com:VictorTsyganov/homework_bot.git ```

Создать и активировать виртуальное окружение:

``` python -m venv venv ``` 

* Если у вас Linux/macOS:
    ``` source venv/bin/activate ``` 

* Если у вас Windows:
    ``` source venv/Scripts/activate ```
    
``` python -m pip install --upgrade pip ``` 

Перейти в папку workshop_repairs в командной строке:

``` cd homework_bot ``` 

Установить зависимости из файла requirements:

``` pip install -r requirements.txt ``` 

Заполнить переменные окружения в .env:

``` PRACTICUM_TOKEN = токен_к_API_Практикум.Домашка ```  
``` TELEGRAM_TOKEN = токен_Вашего_Telegtam_бота ```  
``` TELEGRAM_CHAT_ID = Ваш_Telegram_ID ```

Запустить программу:

``` python homework.py ```

## Системные требования
- Python 3.9+
- Works on Linux, Windows, macOS

## Стек технологий

- Python 3.9

- python-telegram-bot 13.7

## Автор

[Виктор Цыганов](https://github.com/VictorTsyganov)
