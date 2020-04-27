from flask import Flask
from threading import Thread
from time import sleep
from random import randint

app = Flask(__name__)
def func():
    while True:
        print(randint(1,5))
        sleep(1)
        t_func.stop()
t_func = Thread(target = func)
@app.route('/')
def start():
    t_func.start()
    return 'hello from Thread 2'


app.run()
