import os
import sqlite3
import datetime
from datetime import date

current_date = str(date.today())
current_date_time = datetime.datetime.now()
current_time = str(current_date_time.time())

def createdb():
    con = sqlite3.connect("res/logs.sqlite")
    # Создание курсора
    cur = con.cursor()
    # таблица 1
    cur.execute("""CREATE TABLE logins (
    id   INTEGER PRIMARY KEY AUTOINCREMENT
                 UNIQUE
                 NOT NULL,
    user STRING,
    date STRING  NOT NULL,
    time STRING  NOT NULL
);
""")
    con.commit()
    # таблица 2
    cur.execute("""CREATE TABLE transfers (
    id        INTEGER PRIMARY KEY AUTOINCREMENT
                      UNIQUE
                      NOT NULL,
    date      STRING  NOT NULL,
    time      STRING  NOT NULL,
    recipient STRING,
    amount    STRING
);
""")
    con.commit()
    con.close()
def transfer_money(recipient, amount):
    # Подключение к БД
    con = sqlite3.connect("res/logs.sqlite")
    # Создание курсора
    cur = con.cursor()
    # запись
    cur.execute("""INSERT INTO transfers(date,time,recipient,amount) VALUES (?, ?, ?, ?)""",
                (current_date, current_time, str(recipient), str(amount)))
    con.commit()
    con.close()


def logins():
    con = sqlite3.connect("res/logs.sqlite")
    # Создание курсора
    cur = con.cursor()
    # запись
    cur.execute("""INSERT INTO logins(user,date,time) VALUES (?, ?, ?)""",
                (os.getlogin(), current_date, current_time))
    con.commit()
    con.close()
