from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime
import json
import os
import glob


# Не могли в POSTMAN'e отправить запрос, выдавало ошибку безопасности. Это типа фикс
@csrf_exempt
def log(request):
    if request.method == 'POST':
        # Получаем тело заголовка HTTP — json, обрабатываем его и запихиваем в словарь
        body = request.body.decode()
        dataDict = json.loads(body)

        # Достаем данные из словаря для дальнейшего использования
        userId = dataDict['id']
        userName = dataDict['user_name']
        timestamp = dataDict['timestamp']
        text = dataDict['text']

        # Переписываем имя в более удобный формат (меняем пробелы на "_") && меняем формат даты на что-то читабельное
        userName = '_'.join(userName.split()).lower()
        dateTime = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        # Переходим из папки запущенног оскрипта в папку с логами
        os.chdir('logger/logs')

        # Получаем полный путь к директории логов
        fullPath = os.getcwd().replace('\\', '/')

        # Задаем имя файла, в который будем помещать данные && прописываем полный путь к этому файлу
        fileName = f'{ userName }-{ userId }.txt'
        filePath = fullPath + '/' + fileName

        # Ищем файл с существующим userId. Проверка на наличие файла идет только по userId, не по ФИО/нику
        # Если он найден, получаем "1" и просто записываем в него новую инфу
        if len(glob.glob(f"*-{ userId }.txt")):

            # Если пользователь сменил имя, то мы все равно получаем доступ к нужному файлу (по userID в названии).
            # Если пользователь сменил имя, то мы переименовываем файл
            oldFileName = glob.glob(f"*-{ userId }.txt")[0]
            oldFilePath = fullPath + '/' + oldFileName
            os.rename(oldFilePath, filePath)

            # По идее открываем файл на дозапись
            f = open(fileName, 'a', encoding='utf-8')

        # Иначе — создаем новый файл.
        else:
            # По идее открываем файл на перезапись и создани, если не существует (по сути — на создание)
            f = open(rf'{ fileName }', 'w', encoding='utf-8')

        # Производим запись в ранее открытый файл и закрываем его
        f.write(f'{ dateTime } \t\t { text }\n')
        f.close()

        # Т.к. мы ранее переходили из дирректории работы данного скрипта в папку с логами, нам нужно вернуться обратно
        os.chdir('../..')

        return HttpResponse('Success!')
