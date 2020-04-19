from flask import Flask, render_template, request, escape, redirect
import vk
from time import sleep
from datetime import datetime
import sys
import vk_api

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello():
    logging(
        operation = 'Hello_page', 
        time = datetime.today())
    return render_template('hello.html')


@app.route('/help')
def help() -> 'html':
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
                               msg='Все заявки успешно приняты')
    except BaseException:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные')


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
                            msg='Все друзья успешно удалены!')
    except:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные')


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
                               msg='Все посты успешно удалены!')
    except BaseException:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные')


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
                               msg='Все посты успешно удалены!')
    except BaseException:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные')


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
                               msg='Все друзья успешно разблокироавны!')
    except BaseException:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные')


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
        # average age
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
        ##
        dat = [0, 0]
        cit = 0
        flag = False
        info = vkapi.users.get(user_ids=user, fields='city,bdate')
        if 'bdate' in info[0].keys():
            if len(info[0]['bdate']) > 5:
                return render_template('smska.html',
                                       title='Успех!',
                                       msg='Год рожедния: ' + str(info[0]['bdate'][-4:]))
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
                                               msg='Год рожедния:' + str(i))
                        flag = True
            if flag:
                break
    except BaseException:
        return render_template('smska.html',
                               title='Упс.. Что-то пошло не так',
                               msg='В случае появления данного окна, вы ввели неверные данные')


@app.route('/viewlog')
def view_the_logs():
    contents = []
    with open('data.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Время', 'IP', 'Браузер', 'ОС', 'Операция', 'Информация о запросе')
    return render_template('viewlog.html',
    title = 'Логи',
    the_row_titles = titles,
    the_data = contents)


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
    with open('data.log', 'w'):
        pass
    return redirect('/viewlog')

if __name__ == '__main__':
    app.run(debug = True)