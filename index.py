# -*- coding: utf-8 -*-
import requests # Библиотека для отправки запросов
import json # Библиотека json
import smtplib # Библиотека для отправки Email
import datetime # Библиотека для работы с датой и временем
import settings # Файл настроек
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jinja2
import time

# Исходные данные
idInstance = settings.idInstance
apiTokenInstance = settings.apiTokenInstance

# Удаления входящего уведомления
def delMess(receiptId):
    url = f"https://api.green-api.com/waInstance{idInstance}/DeleteNotification/{apiTokenInstance}/{receiptId}"
    payload = {}
    headers = {}
    requests.request("DELETE", url, headers=headers, json=payload)

# Получение информации о группе
def groupInfo(groupNumber):
    url = f"https://api.green-api.com/waInstance{idInstance}/getGroupData/{apiTokenInstance}"
    payload = {'groupId': groupNumber}
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, json=payload)
    groupInfoChat = json.loads(response.text)
    return groupInfoChat['subject']

# Функция для отправки файла Excel с отчетом на почту
def sendTable(listMain):
    SENDER_EMAIL = settings.sender
    SENDER_PASSWORD = settings.sender_password
    SERVER = 'smtp.yandex.ru'
    RECEIVER_EMAIL = settings.to_item

    SUBJECT = 'Отчет с найденными словами'
    tpl = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        <style type="text/css">
      table {
        background: white;
        border-radius:3px;
        border-collapse: collapse;
        height: auto;
        max-width: 900px;
        padding:5px;
        width: 100%;
        animation: float 5s infinite;
      }
      th {
        color:#D5DDE5;;
        background:#1b1e24;
        border-bottom: 4px solid #9ea7af;
        font-size:14px;
        font-weight: 300;
        padding:10px;
        text-align:center;
        vertical-align:middle;
      }
      tr {
        border-top: 1px solid #C1C3D1;
        border-bottom: 1px solid #C1C3D1;
        border-left: 1px solid #C1C3D1;
        color:#000000;
        font-size:16px;
        font-weight:bold;
      }
      td {
        background:#FFFFFF;
        padding:10px;
        text-align:left;
        vertical-align:middle;
        font-weight:300;
        font-size:13px;
        border-right: 1px solid #C1C3D1;
      }
    </style>
      </head>
      <body>
        <table>
          <thead>
            <tr style="border: 1px solid #1b1e24;">
              <th>Номер телефона</th>
              <th>Имя клиента</th>
              <th>Сообщение</th>
              <th>Номер чата</th>
              <th>Дата</th>
              <th>Название чата</th>
            </tr>
          </thead>
          <tbody>
            {% for i in listMain %}
                <tr>
                {% for k in i %}
                    <td>{{k}}</td>
                {% endfor %}
                </tr>
            {% endfor %}
          </tbody>
        </table>
        <br>
        <br>
        -------------------------------------<br>
        Создание и разработка чат-ботов:<br>
        Телефон: +7 (347) 222-20-21<br>
        Почта: zakaz@soft-servis.ru<br>
        Адрес: г. Уфа, ул.Менделеева 134/7, 413 офис<br>
      </body>
    </html>
    """

    HTML = jinja2.Template(tpl).render(listMain=listMain)

    def _generate_message() -> MIMEMultipart:
        message = MIMEMultipart("alternative", None, [MIMEText(HTML, 'html')])
        message['Subject'] = SUBJECT
        message['From'] = SENDER_EMAIL
        message['To'] = RECEIVER_EMAIL
        return message

    def send_message():
        message = _generate_message()
        server = smtplib.SMTP(SERVER)
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        server.quit()

    send_message()

# Функция для отправки статуса на электронную почту
def emailStatus(statusCheck):
    sender = settings.sender # Email от кого отправляем письмо
    sender_password = settings.sender_password # Пароль от почты
    to_item = settings.to_item # Email кому отправляем
    mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    mail_lib.login(sender, sender_password)
    msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
    sender, to_item, statusCheck)
    msg += 'Это уведомление о статусе телефона, если пришло данное сообщение, значит есть проблемы с телефоном' + '\r\n' + 'Статус телефона: ' + statusCheck + '\r\n' + 'Информация для связи:' + '\r\n' + 'Телефон: +7 (347) 222-20-21' + '\r\n' +  'Почта: zakaz@soft-servis.ru' + '\r\n' + 'Адрес: г. Уфа, ул.Менделеева 134/7, 413 офис'  # Текст сообщения
    mail_lib.sendmail(sender, to_item, msg.encode('utf8'))
    mail_lib.quit()

def emailMessages(numberPhone, nameClient, textMessClient, numberChats, dateMess, chatName):
    sender = settings.sender # Email от кого отправляем письмо
    sender_password = settings.sender_password # Пароль от почты
    to_item = settings.to_item # Email кому отправляем
    mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    mail_lib.login(sender, sender_password)
    msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
    sender, to_item, nameClient)
    msg += 'Номер телефона: ' + numberPhone + '\r\n' + 'Имя клиента: ' + nameClient + '\r\n' + 'Текст сообщения: ' + textMessClient + '\r\n' + 'Номер чата: ' + numberChats + '\r\n' + 'Дата сообщения: ' + dateMess + '\r\n' + 'Название чата: ' + chatName + '\r\n' + '\r\n' + 'Создание и разработка чат-ботов:' + '\r\n' + 'Телефон: +7 (347) 222-20-21' + '\r\n' + 'Почта: zakaz@soft-servis.ru' + '\r\n' + 'Адрес: г. Уфа, ул.Менделеева 134/7, 413 офис'  # Текст сообщения
    mail_lib.sendmail(sender, to_item, msg.encode('utf8'))
    mail_lib.quit()

# Функция для поиска ключевых слов в чатах
def findKeysChats():
    # Прочтение ключевых слов из текстового файла
    listMain = []
    file1 = open("keys.txt", "r", encoding="utf-8") # Открываем файл с ключевыми словами
    findKeys = [] # Объявляем пустой список

    while True:
        line = file1.readline()  # Считываем строку
        if not line: # Прерываем цикл, если строка пустая
            break
        findKeys.append(line.strip()) # Добавляем ключевое слово в список

    file1.close # Закрываем файл
    getNewMess(findKeys, listMain) # Вызов функции по поиску слов с сообщениях

# Получение последних сообщений
def getNewMess(findKeys, listMain):
    url = f"https://api.green-api.com/waInstance{idInstance}/ReceiveNotification/{apiTokenInstance}"

    payload = {}
    headers= {}
    listGal = []
    response = requests.request("GET", url, headers=headers, json=payload)

    try:
        tets = json.loads(response.text)
        for searchKey in findKeys:
            if tets['body']['typeWebhook'] == 'incomingMessageReceived' and tets['body']['messageData']['typeMessage'] == 'textMessage' and len(tets['body']['senderData']['chatId']) > 18 and tets['body']['messageData']['textMessageData']['textMessage'].find(searchKey) != -1:
                print('Нашлось ключевое слово')
                numberPhone = str(tets['body']['senderData']['sender'].replace('@c.us', ''))
                print('Номер телефона:', tets['body']['senderData']['sender'].replace('@c.us', ''))
                if tets['body']['senderData']['senderName'] != '':
                    nameClient = str(tets['body']['senderData']['senderName'])
                    print('Имя:', tets['body']['senderData']['senderName'])
                else:
                    nameClient = 'Имя не определенно'
                    print('Имя:', 'Не определенно')
                textMessClient = str(tets['body']['messageData']['textMessageData']['textMessage'])
                print('Полное сообщение:', tets['body']['messageData']['textMessageData']['textMessage'])
                numberChats = str(tets['body']['senderData']['chatId'])
                print('Номер чата:', tets['body']['senderData']['chatId'])
                dateMess = str(datetime.datetime.fromtimestamp(tets['body']['timestamp']))
                print('Дата и время:', datetime.datetime.fromtimestamp(tets['body']['timestamp']))
                if (len(numberChats) > 16):
                    chatName = str(groupInfo(numberChats))
                    print('Название группы:', chatName)
                else:
                    chatName = 'None'
                    print('Название группы:', 'None')

                listGal.append(numberPhone)  # Добавление Номера телефона в список
                listGal.append(nameClient)  # Добавление Имя клиента в список
                listGal.append(textMessClient)  # Добавление Текста сообщения в список
                listGal.append(numberChats)  # Добавление Номера чата в список
                listGal.append(dateMess)  # Добавление Даты отправки сообщения в список
                listGal.append(chatName)  # Добавление Названия группы в список
                listMain.append(listGal)  # Добавление данных об сообщений в один общий список
                print(listMain)
                print(listGal)
                #time.sleep(3)  # Сон на 3 секунды
                delMess(tets['receiptId'])  # Вызов функции по удалению уведомления
                #time.sleep(3)  # Сон на 3 секунды

        else:
            print('Нет слова')
            delMess(tets['receiptId'])
            #time.sleep(1)
        getNewMess(findKeys, listMain)  # Заново вызов функции, по поиску новых уведомлений
    except Exception as ex:
        print(ex)
        if len(listMain) == 0:
            print('Нет данных')
        else:
            print('Полный список', listMain)
            sendTable(listMain)


def start(event, context):
    # Проверка статуса телефона
    urlStatus = f"https://api.green-api.com/waInstance{idInstance}/getStateInstance/{apiTokenInstance}"

    payload = {}
    headers= {}

    response = requests.request("GET", urlStatus, headers=headers, json=payload)
    textResponse = json.loads(response.text)

    if textResponse['stateInstance'] == 'authorized':
        print(textResponse['stateInstance'])
        findKeysChats() # Вызов функции поиск ключевых слов
    elif textResponse['stateInstance'] == 'notAuthorized':
        print(textResponse['stateInstance'])
        emailStatus('Телефон не авторизован') # Отправка сообщения об ошибке на почту
    elif textResponse['stateInstance'] == 'sleepMode':
        print(textResponse['stateInstance'])
        emailStatus('Телефон в спящем режиме') # Отправка сообщения об ошибке на почту