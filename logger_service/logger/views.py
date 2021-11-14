from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
import json
import os.path


@csrf_exempt
def log(request):
    if request.method == 'POST':
        body = request.body.decode()
        dataDict = json.loads(body)
        name = dataDict['name']
        date = dataDict['date']
        chatID = dataDict['chatID']
        content = dataDict['content']

        fullPath = 'F:/Web/logger-service/logger_service/logger/logs/'
        # fullPath = 'F:\Web\logger-service\logger_service\logger\logs\\'
        fileName = f'{ fullPath + name.lower() }.txt'

        # try:
        #     f = open(fileName, 'a')
        #     f.close()
        # except FileNotFoundError:
        #     f = open(fileName, 'w')
        #
        #     f.close()
        # else:
        #     f = open('log.txt', 'a')
        #     f.write(f'Время: {date}\nФИО: {name}\nChat_ID: {chatID}\nТекст сообщения:{content}')

        if os.path.exists(fileName):
            f = open(fileName, 'a', encoding='utf-8')
        else:
            f = open(fileName, 'w')

        f.write(f'Время: { date }\nФИО: { name }\nChat_ID: { chatID }\nТекст сообщения:{ content }\n\n\n')
        f.close()


        return HttpResponse('Success!')
