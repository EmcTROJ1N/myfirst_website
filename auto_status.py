import requests as req
import datetime
import urllib
import json
from time import sleep
import vk

token = "63eae9c58bbda1b7cf0c7d41c1075a726f743f1c3168dbf7e11e7761ad973b6e7b115ea7bf6453bc4c9f5" #Сюда вводим свой токен.
timeKD = 60 #Сюда вводим время обновления статуса.(Время в секундах)

def startStatus():
    getCountry = req.get(f"https://api.vk.com/method/account.getProfileInfo?v=5.95&access_token={token}").json()
    try:
        city = getCountry["response"]["city"]["title"]
    except KeyError:
        print("У профиля не указан город, по умолчанию была выбрана Москва.")
        city = "Москва"

    data = req.get("http://api.openweathermap.org/data/2.5/weather",
    params = {"q": city,
              "appid": "778d98cf94b6609bec655b872f24b907",
              "units": "metric",
              "lang": "ru"}).json()
    try:
        getLikes = req.get(f"https://api.vk.com/method/photos.get?album_id=profile&rev=1&extended=1&count=1&v=5.95&access_token={token}").json()
        getLikes = getLikes["response"]["items"][0]["likes"]["count"]
    except IndexError:
        print("У профиля отсутсвует аватар или лайки.")
        getLikes = 0

    getValuts = req.get("https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=6780a6de85b0690a6e0f02e6fc5bfd4f").json().get("data")

    today = datetime.datetime.today()
    nowTime = today.strftime("%H:%M")
    nowDate = today.strftime("%d.%m.%Y")

    statusSave = ("Время: {0} | Дата: {1} | Погода в '{2}': {3}℃ | Лайков на аве: {4}".format(nowTime, nowDate,
        data["name"], str(data["main"]["temp"]), getLikes))
    statusOut = req.get(f"https://api.vk.com/method/status.set?text={statusSave}&v=5.95&access_token={token}").json()
    if statusOut.get("error", None):
        print(f"Не удалось обновить статус сервер вернул неверный код ответа: {statusOut}")
    else:
        print(f"Статус был обновлен")

while True:
    startStatus()
    sleep(timeKD)