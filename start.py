#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, escape, redirect, session, copy_current_request_context
import vk
from time import sleep
from datetime import datetime
import sys
import vk_api
import urllib
import json
import requests as req
from threading import Thread

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello():
    logging(
        operation = 'Hello_page',
        time = datetime.today())
    return render_template('hello.html')


@app.route('/help')
def help() :
    return render_template('help.html')


@app.route('/auto_invite')
def auto_invite():
    return render_template('entry_token.html',
                           title='Автоматический прием заявок в друзья',
                           url='/auto_invite_start')


@app.route('/auto_invite_start', methods=['POST', 'GET'])
def start_auto_invite():
    try:
        vk = vk_api.VkApi(token=request.form['token'])
        print("\nЗаявок в друзья: " +
              str(vk.method("users.getFollowers", {"count": 1})["count"]) +
              "\n")
        id2 = 0
        while True:
            followers_count = vk.method(
                "users.getFollowers", {
                    "count": 1})["count"]
            if followers_count > 0:
                id = vk.method("users.getFollowers", {"count": 1})["items"][0]
                if id != id2 or id2 == 0:
                    id2 = id
                    print("Новая заявка в друзья, id пользователя " + str(id))
                    try:
                        vk.method("friends.add", {"user_id": id})
                        print(
                            "Добавил пользователя c id " +
                            str(id) +
                            " в друзья\n")
                    except BaseException:
                        try:
                            vk.method("account.ban", {"owner_id": id})
                            print(
                                "Пользователь с id " +
                                str(id) +
                                " добавлен в чёрный список\n")
                        except BaseException:
                            break
            else:
                break
        logging(operation = 'Auto_invite_friends',
        time = datetime.today())
        return render_template('smska.html',
                               title='Успех',
                               msg='Все заявки успешно приняты',
                               url = '/')
    except BaseException:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные',
                               url = '/')


@app.route('/delete_all_friends')
def deletefriends():
    return render_template('entry_token.html',
                           title='Удаление всех ваших друзей',
                           url='/delete_fr_start')


@app.route('/delete_fr_start', methods=['POST', 'GET'])
def start_delete():
    try:
        session = vk.Session(access_token=request.form['token'])
        api = vk.API(session, scope='friends', v='5.62')
        friends = api.friends.get()
        for i in friends['items']:
            api.friends.delete(user_id=i)
        logging(operation = 'Delte_all_friends',
        time = datetime.today())
        return render_template('smska.html',
                            title='Успех!',
                            msg='Все друзья успешно удалены!',
                            url = '/')
    except:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные',
                               url = '/')


@app.route('/wall_clear')
def wall_clear():
    return render_template('entry_token.html',
                           title='Очистка вашей стены ВКонтакте',
                           url='/start_clear_wall')


@app.route('/start_clear_wall', methods=['POST'])
def start_clear_wall():
    try:
        session = vk.Session(access_token=request.form['token'])
        api = vk.API(session, scope='wall', v='5.62')
        mywall = api.wall.get()
        page_id = api.users.get()
        for i in range(mywall['count']):
            api.wall.delete(
                post_id=mywall['items'][i]['id'],
                owner_id=page_id[0]['id'])
        logging(operation = 'Clear_wall',
        time = datetime.today())
        return render_template('smska.html',
                               title='Успех!',
                               msg='Все посты успешно удалены!',
                               url = '/')
    except BaseException:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные',
                               url = '/')


@app.route('/entry_spam_groups', methods=['POST', 'GET'])
def entry_spam_groups() -> 'html':
    return render_template('entry-spam-groups.html',
                           the_title='Спамер коментариями ВКонтакте')


@app.route('/spam_groups', methods=['POST', 'GET'])
def start_spam():
    try:
        session = vk.Session(access_token=request.form['token'])
        api = vk.API(session, scope='wall', v='5.62')
        for i in range(int(request.form['k'])):
            api.wall.createComment(
                owner_id=str(
                    '-' + request.form['group_id']),
                post_id=request.form['post_id'],
                message=request.form['to_write'])
            sleep(int(request.form['timing']))
        logging(operation = 'Spam_groups',
        time = datetime.today())
        return render_template('smska.html',
                               title='Успех!',
                               msg='Все посты успешно удалены!',
                               url = '/')
    except BaseException:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные',
                               url = '/')


@app.route('/clear_CHS')
def entry_clear_CHS():
    return render_template('entry_token.html',
                           title='Очистка вашего черного списка',
                           url='/clear_CHS_start')


@app.route('/clear_CHS_start', methods=['POST'])
def start_clear_CHS():
    try:
        session = vk.Session(access_token=request.form['token'])
        api = vk.API(session, scope='friends', v='5.62')

        banned = api.account.getBanned()
        for i in range(banned['count']):
            api.account.unban(owner_id=banned['items'][i]['id'])
        logging(operation = 'clear_my_Black_List',
        time = datetime.today())
        return render_template('smska.html',
                               title='Успех!',
                               msg='Все друзья успешно разблокироавны!',
                               url = '/')
    except BaseException:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные',
                               url = '/')


@app.route('/entry_birthday')
def entry_birthday():
    return render_template('entry_birthday.html',
                           title='Поиск скрытой даты рождения ВК',
                           url='/start_find_birthday')


@app.route('/start_find_birthday', methods=['POST'])
def start_find_day():
    try:
        session = vk.Session(access_token=request.form['token'])
        vkapi = vk.API(session, v='5.53')
        logging(operation = 'Find_year_birthday',
        time = datetime.today())
        user = request.form['day_id']
        friends = vkapi.friends.get(user_id=user, fields='bdate')
        bdates = 0
        counter = 0
        if friends['count'] > 0:
            for i in friends['items']:
                if 'bdate' in i.keys():
                    if len(i['bdate']) > 5:
                        bdates += int(i['bdate'][-4:])
                        counter += 1
            avr = bdates // counter
        else:
            avr = 1990
        ageFromTo = [avr]
        for i in range(1, 40):
            ageFromTo.append(avr + i)
            ageFromTo.append(avr - i)
        dat = [0, 0]
        cit = 0
        flag = False
        info = vkapi.users.get(user_ids=user, fields='city,bdate')
        if 'bdate' in info[0].keys():
            if len(info[0]['bdate']) > 5:
                return render_template('smska.html',
                                       title='Успех!',
                                       msg='Год рожедния: ' + str(info[0]['bdate'][-4:]),
                                       url = '/')
            dat = info[0]['bdate'].split('.')
        if 'city' in info[0].keys():
            cit = info[0]['city']['id']
        fname = info[0]['first_name']
        lname = info[0]['last_name']
        for i in ageFromTo:
            while True:
                try:
                    ans = vkapi.users.search(q=fname + ' ' + lname, count=1000,
                                             birth_day=dat[0], birth_month=dat[1],
                                             city=0, birth_year=i)
                    break
                except vk.exceptions.VkAPIError as text:
                    if str(text)[:2] == '6.':
                        sleep(1)
                        continue
            if ans['count'] > 0:
                for j in ans['items']:
                    if str(j['id']) == user:
                        return render_template('smska.html',
                                               title='Успех!',
                                               msg='Год рожедния:' + str(i),
                                               url = '/')
                        flag = True
            if flag:
                break
    except BaseException:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные',
                               url = '/')


@app.route('/auto_online', methods = ['POST', 'GET'])
def auto_online():
    return render_template('entry_token.html',
    title = 'Вечный онлайн для вашей страницы ВК',
    url = '/auto_online_start')


@app.route('/auto_online_start', methods = ['POST'])
def auto_online_start():
    @copy_current_request_context
    def t_auto_online(token):
        try:
            time_now = datetime.today()
            session = vk.Session(access_token = token)
            logging(operation = 'Auto_online',
                time = time_now)
            api = vk.API(session, v = "5.95")
            while True:
                exit = api.account.setOnline(voip = 0)
                sleep(180)
                if time == datetime.today():
                    break
        except BaseException:
            return render_template('smska.html',
                                   title='Упс.. Что-то пошло не так',
                                   msg='В случае появления данного окна, вы ввели неверные данные',
                                   url = '/')
    auto_online_thread = Thread(target = t_auto_online, args = (request.form['token'],))
    auto_online_thread.start()
    return render_template('smska.html',
    title = 'Успех',
    msg = 'Все работает, можете идти пить чай)',
    url = '/')


@app.route('/auto_status')
def auto_status():
    return render_template('entry_token.html',
    title ='Автоматическое обновление статуса',
    url = '/auto_status_start')


@app.route('/auto_status_start', methods = ['POST'])
def start_auto_status():
    try:
        logging(operation = 'Auto_online',
            time = datetime.today())
        while True:
            startStatus(request.form['token'])
            sleep(60)
    except BaseException:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные',
                               url = '/')


def startStatus(token):
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

    today = datetime.today()
    nowTime = today.strftime("%H:%M")
    nowDate = today.strftime("%d.%m.%Y")

    statusSave = ("Время: {0} | Дата: {1} | Погода в '{2}': {3}℃ | Лайков на аве: {4}".format(nowTime, nowDate,
        data["name"], str(data["main"]["temp"]), getLikes))
    statusOut = req.get(f"https://api.vk.com/method/status.set?text={statusSave}&v=5.95&access_token={token}").json()
    if statusOut.get("error", None):
        print(f"Не удалось обновить статус сервер вернул неверный код ответа: {statusOut}")
    else:
        print(f"Статус был обновлен")


@app.route('/viewlog')
def view_the_logs():
    if 'logged_in' in session:
        contents = []
        with open('data.log') as log:
            for line in log:
                contents.append([])
                for item in line.split('|'):
                    contents[-1].append(escape(item))
        titles = ('Время', 'IP', 'Браузер', 'ОС', 'Операция', 'Информация о запросе')
        if int(session['lvl']) >= 2:
            return render_template('viewlog.html',
            title = 'Логи',
            the_row_titles = titles,
            the_data = contents)
        else:
            return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Ваш уровень доступа не соответствует минимальному',
                               url = '/admin_panel')
    else:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Кажись кто-то забыл авторизироаться!',
                               url = '/')


def logging(operation, time):
    with open('data.log', 'a') as log:
        print(time, end = '|', file = log)
        print(request.environ['HTTP_X_FORWARDED_FOR'], end = '|', file = log)
        print(request.user_agent.browser, end = '|', file = log)
        print(request.user_agent.platform, end = '|', file = log)
        print(operation, end = '|', file = log)
        print(request.form, end = '|\n', file = log)


@app.route('/viewlog_accounts')
def view_the_acctounts():
    if 'logged_in' in session:
        contents = []
        with open('accounts.log') as log:
            for line in log:
                contents.append([])
                for item in line.split('|'):
                    contents[-1].append(escape(item))
        titles = ('Логин', 'Пароль', 'LVL доступа')
        if int(session['lvl']) >= 2:
            return render_template('viewlog.html',
            title = 'Логи',
            the_row_titles = titles,
            the_data = contents)
        else:
            return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Ваш уровень доступа не соответствует минимальному',
                               url = '/admin_panel')
    else:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Кажись кто-то забыл авторизироаться!',
                               url = '/')


def logging(operation, time):
    with open('data.log', 'a') as log:
        print(time, end = '|', file = log)
        print(request.environ['HTTP_X_FORWARDED_FOR'], end = '|', file = log)
        print(request.user_agent.browser, end = '|', file = log)
        print(request.user_agent.platform, end = '|', file = log)
        print(operation, end = '|', file = log)
        print(request.form, end = '|\n', file = log)



@app.route('/clear_logs')
def clear_log():
    if 'logged_in' in session:
        if int(session['lvl']) >= 3:
            with open('data.log', 'w'):
                pass
            return redirect('/viewlog')
        else:
            return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Ваш уровень доступа не соответствует минимальному',
                               url = '/admin_panel')



@app.route('/login')
def login():
    if 'logged_in' in session:
        if int(session['lvl']) >= 1:
            return redirect('/admin_panel')
        else:
            return render_template('login.html',
            title = 'Авторизация')
    else:
        return render_template('login.html',
        title = 'Авторизация')


@app.route('/login_check', methods = ['POST'])
def login_check():
    with open('accounts.log', 'r') as acc:
        for i in acc:
            login_passwd = i.split('|')
            lvl = login_passwd[2][:-1]
            if request.form['login'] == login_passwd[0]:
                if request.form['passwd'] == login_passwd[1]:
                    session['logged_in'] = True
                    session['lvl'] = lvl
                    session['login'] = request.form['login']
                    session['passwd'] = request.form['passwd']
                    return redirect('/admin_panel')
    return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные',
                               url = '/login')


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
        return redirect('/')
        return render_template('smska.html',
        title = 'Вы никуда и не входили',
        msg = 'Могу порекомендовать выйти в окно!',
        url = '/')



@app.route('/admin_panel', methods = ['POST', 'GET'])
def admin_panel():
    if 'logged_in' in session:
        if int(session['lvl']) >= 1:
            return render_template('admin-panel.html',
            title = 'Админ панель',
            login = session['login'],
            passwd = session['passwd'],
            lvl = session['lvl'])
        else:
            return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Ваш уровень доступа не соответствует минимальному',
                               url = '/')
    else:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Кажись кто-то забыл авторизироаться!',
                               url = '/')

@app.route('/registrate', methods = ['POST', 'GET'])
def registrate():
    if 'logged_in' in session:
        if int(session['lvl']) >= 1:
            return render_template('registrate.html',
            title = 'Регистрация нового пользователя',
            url = '/start_registrate')
        else:
            return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Ваш уровень доступа не соответствует минимальному',
                               url = '/admin_panel')
    else:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Кажись кто-то забыл авторизироаться!',
                               url = '/')


@app.route('/start_registrate', methods = ['POST'])
def start_registrate():
    if int(request.form['lvl']) > 3:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Такого уровня доступа не существует!',
                               url = '/admin_panel')
    with open('accounts.log', 'r') as acc:
        for i in acc:
            login_passwd = i.split('|')
            if request.form['login'] == login_passwd[0]:
                return render_template('smska.html',
                                    title='Упс.. Что-то пошло не так',
                                    msg='Такой логин уже существует!',
                                    url = '/registrate')
    with open('accounts.log', 'a') as acc:
        print(request.form['login'] + '|' + request.form['passwd'] + '|' + request.form['lvl'], file = acc)
    return render_template('smska.html',
        title = 'Успех',
        msg = 'Аккаунт успешно зарегестрирован!',
        url = '/admin_panel')



@app.route('/chng_passwd')
def chng_passwd():
    if 'logged_in' in session:
        if int(session['lvl']) >= 1:
            return render_template('chng_passwd.html')
        else:
            return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Ваш уровень доступа не соответствует минимальному',
                               url = '/admin_panel')
    else:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Кажись кто-то забыл авторизироаться!',
                               url = '/')

@app.route('/chng_passwd_start', methods = ['POST'])
def start_chng():
    with open ('accounts.log', 'r') as f:
        old_data = f.read()
    new_data = old_data.replace(request.form['login'] + '|' + request.form['passwd'], request.form['login'] + '|' + request.form['new_passwd'])
    with open ('accounts.log', 'w') as f:
        f.write(new_data)
    return render_template('smska.html',
                            title = 'Успех',
                            msg = 'Пароль успешно изменен!',
                            url = '/admin_panel')


@app.route('/rm_passwd', methods = ['POST', 'GET'])
def rm_passwd():
    if 'logged_in' in session:
        if int(session['lvl']) >= 3:
            return render_template('rm_passwd.html',
            title = 'Удаление аккаунта',
            url = '/rm_passwd_start')
        else:
            return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Ваш уровень доступа не соответствует минимальному',
                               url = '/admin_panel')
    else:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Кажись кто-то забыл авторизироаться!',
                               url = '/')


@app.route('/rm_passwd_start', methods = ['POST', 'GET'])
def rm_chng():
    with open ('accounts.log', 'r') as f:
        old_data = f.read()
        print(old_data)
        new_data = old_data.replace(request.form['login'] + '|' + request.form['passwd'] + '|' + request.form['lvl'] + '\n', '')
        print(new_data)
    with open ('accounts.log', 'w') as f:
        f.write(new_data)
    return render_template('smska.html',
                            title = 'Успех',
                            msg = 'Аккаунт успешно удален!',
                            url = '/admin_panel')

@app.route('/chng_lvl')
def chng_lvl():
    if 'logged_in' in session:
        if int(session['lvl']) >= 3:
            return render_template('chng_lvl.html')
        else:
            return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Ваш уровень доступа не соответствует минимальному',
                               url = '/admin_panel')
    else:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='Кажись кто-то забыл авторизироваться!',
                               url = '/')


@app.route('/chng_lvl_start', methods = ['POST'])
def chng_lvl_start():
    with open ('accounts.log', 'r') as f:
        old_data = f.read()
        print(old_data)
        new_data = old_data.replace(request.form['login'] + '|' + request.form['passwd'] + '|' + request.form['lvl'] + '\n', request.form['login'] + '|' + request.form['passwd'] + '|' + request.form['new_lvl'] + '\n')
        print(new_data)
    with open ('accounts.log', 'w') as f:
        f.write(new_data)
    return render_template('smska.html',
                            title = 'Успех',
                            msg = 'Уровень доступа успешно изменен',
                            url = '/admin_panel')

app.secret_key = 'itisverysecretkey'
if __name__ == '__main__':
    app.run()
