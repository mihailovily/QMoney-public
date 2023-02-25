import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtWidgets import QInputDialog

import antipirate
import number
import pyqiwi
import db_edit
import os.path


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # окошко
        self.setFixedSize(350, 300)
        self.setWindowTitle('QMoney')
        self.setWindowIcon(QIcon('favicon.ico'))
        # кнопка
        self.button_license = QPushButton(self)
        self.button_license.move(100, 150)
        self.button_license.setText("Выбрать файл лицензии")
        self.button_license.clicked.connect(self.license)
        # картинка
        self.pixmap = QPixmap('res/m_qiwi.png')
        self.image = QLabel(self)
        self.image.move(10, 10)
        self.image.resize(128, 58)
        self.image.setPixmap(self.pixmap)
        if os.path.exists("res/logs.sqlite") != True:
            db_edit.createdb()
        # запись в бд о входе
        db_edit.logins()

    def get_phone(self):
        phone, ok_pressed = QInputDialog.getText(self, "Телефон",
                                                 "Введи номер телефона, привязанный к qiwi")
        if ok_pressed:
            if not number.checknum(phone):
                self.get_phone()
            else:
                self.phone = number.checknum(phone)
                self.get_api()

    def get_api(self):
        api, ok_pressed = QInputDialog.getText(self, "QIWI API",
                                               "Введи QIWI API token")
        if ok_pressed:
            # если все ок, идем дальше, иначе ждем ввода верного апи
            try:
                self.api = api
                self.twoWindow = Cabinet(self.api, self.phone)
                self.twoWindow.show()
                self.close()
            except:
                self.get_api()

    def license(self):
        # проверка лицензии. если все хорошо, то идем дальше
        # в ином случае стучим на почту
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Лицензия (*.txt);;Все файлы (*)')[0]
        if antipirate.check_license(fname) is True:
            self.get_phone()
        else:
            antipirate.no_license_alarm()


class Cabinet(QWidget):
    def __init__(self, api, phone):
        super().__init__()
        # переменные
        self.wallet = pyqiwi.Wallet(token=api, number=phone)
        self.api = api
        self.phone = phone
        self.initUI()

    def initUI(self):
        # окошко
        self.setFixedSize(350, 300)
        self.setWindowTitle('QMoney')
        self.setWindowIcon(QIcon('favicon.ico'))
        # перевод
        self.button_send = QPushButton(self)
        self.button_send.move(250, 100)
        self.button_send.setText("Перевести")
        self.button_send.clicked.connect(self.send_money)
        # назначение
        self.label_recipient = QLabel(self)
        self.label_recipient.setText('Кому: ')
        self.label_recipient.move(10, 80)
        self.recipient_input = QLineEdit(self)
        self.recipient_input.move(70, 80)
        # сумма
        self.label_how = QLabel(self)
        self.label_how.setText('Сколько: ')
        self.label_how.move(10, 120)
        self.sum_input = QLineEdit(self)
        self.sum_input.move(70, 120)
        # картинка
        self.pixmap = QPixmap('res/m_qiwi.png')
        self.image = QLabel(self)
        self.image.move(10, 10)
        self.image.resize(128, 58)
        self.image.setPixmap(self.pixmap)
        # информация
        self.label_phone = QLabel(self)
        self.label_phone.setText('Номер: +' + str(self.phone))
        self.label_phone.move(200, 10)
        self.label_balance = QLabel(self)
        self.label_balance.setText('Баланс: ' + str(self.wallet.balance()))
        self.label_balance.move(200, 30)

    def send_money(self):
        r = str(self.recipient_input.text())  # получатель
        a = str(self.sum_input.text())  # сумма
        db_edit.transfer_money(r, a)  # запись в бд
        try:
            # отправляем
            self.wallet.send(pid='99', recipient=r, amount=a, comment='Переведено с помощью QMoney')
            self.label_balance.setText('Баланс: ' + str(self.wallet.balance()))
        except:
            pass

    def mouseDoubleClickEvent(self, event):
        # если двойной клик правой мышкой в окне переводов, то генерируем новую лицензию
        if event.button() == Qt.RightButton:
            antipirate.generate_license('newlicense.txt')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec_())
