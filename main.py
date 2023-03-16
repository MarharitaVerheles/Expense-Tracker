from PyQt5 import QtWidgets, QtCore, QtGui, QtSql
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
import sqlite3 as sq
import datetime
import sys
from db_connection import Connection
from db_connection import Analitycs

import matplotlib.pyplot as plt

class MainWindow_UI(QMainWindow):
        def __init__(self):
                super(MainWindow_UI, self).__init__()
                loadUi('Exp_Track_Interface.ui', self)

                self.dateEdit.setMinimumDate(QDate(1999, 1, 1))
                self.dateEdit.setMaximumDate(QDate(2100, 1, 1))
                self.dateEdit.setDate(datetime.date.today())

                self.dateEdit_2.setMinimumDate(QDate(1999, 1, 1))
                self.dateEdit_2.setMaximumDate(QDate(2100, 1, 1))
                self.dateEdit_2.setDate(datetime.date.today())

                self.dateEdit_3.setMinimumDate(QDate(1999, 1, 1))
                self.dateEdit_3.setMaximumDate(QDate(2100, 1, 1))
                self.dateEdit_3.setDate(datetime.date.today())

                #self.label_6.setText(" ")

                self.pushButton.clicked.connect(lambda: app.exit())
                self.pushButton_2.clicked.connect(lambda: self.showMaximized())
                self.pushButton_3.clicked.connect(lambda: self.showMinimized())
                self.Side_Menu_Num = 0
                self.toolButton_5.clicked.connect(lambda: self.Side_Menu_Def_0())

                self.Expense_Tracker = Connection()
                self.Analis = Analitycs()

                self.pushButton_5.clicked.connect(self.save_changes)
                self.update_button.clicked.connect(self.show_data)
                #self.pushButton_6.clicked.connect(self.sum_all)
                self.pushButton_7.clicked.connect(self.count)
                self.pushButton_6.clicked.connect(self.all_ctg)

                self.comboBox.addItems(["Їжа", "Краса і здоров'я", "Розваги", "Шоппінг",
                                        "Підписки", "Комунальні платежі", "Інше"])
                self.comboBox_2.addItems(["Їжа", "Краса і здоров'я", "Розваги", "Шоппінг",
                                          "Підписки", "Комунальні платежі", "Інше"])


                self.toolButton_6.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.add_db))
                self.toolButton_7.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.show_db))
                self.toolButton_9.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.statistic))

                self.tracker_base.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.show()

        def show_data(self):
                data = self.Expense_Tracker.show_data()
                i = len(data)
                self.tracker_base.setRowCount(i)
                tabelrow = 0
                for row in data:
                        self.tracker_base.setItem(tabelrow, 0, QtWidgets.QTableWidgetItem(row[0]))
                        self.tracker_base.setItem(tabelrow, 1, QtWidgets.QTableWidgetItem(row[1]))
                        item = QTableWidgetItem()
                        item.setData(QtCore.Qt.DisplayRole, row[2])
                        self.tracker_base.setItem(tabelrow, 2, item)
                        self.tracker_base.setItem(tabelrow, 3, QtWidgets.QTableWidgetItem(row[3]))
                        tabelrow += 1

        def save_changes(self):
                date = self.dateEdit.date().toPyDate()
                category = self.comboBox.currentText()
                price = self.lineEdit.text()
                description = self.lineEdit_2.text()
                if price!= '':
                        self.Expense_Tracker.insert_data(date, category, price, description)
                        self.lineEdit.clear()
                        self.lineEdit_2.clear()
                        self.dateEdit.setDate(datetime.date.today())


        def Side_Menu_Def_0(self):
                if self.Side_Menu_Num == 0:
                        self.animation1 = QtCore.QPropertyAnimation(self.frame_4, b"maximumWidth")
                        self.animation1.setDuration(500)
                        self.animation1.setStartValue(30)
                        self.animation1.setEndValue(150)
                        self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                        self.animation1.start()

                        self.animation2 = QtCore.QPropertyAnimation(self.frame_4, b"minimumWidth")
                        self.animation2.setDuration(500)
                        self.animation2.setStartValue(30)
                        self.animation2.setEndValue(150)
                        self.animation2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                        self.animation2.start()
                        self.Side_Menu_Num = 1
                else:
                        self.animation1 = QtCore.QPropertyAnimation(self.frame_4, b"maximumWidth")
                        self.animation1.setDuration(500)
                        self.animation1.setStartValue(150)
                        self.animation1.setEndValue(30)
                        self.animation1.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                        self.animation1.start()

                        self.animation2 = QtCore.QPropertyAnimation(self.frame_4, b"minimumWidth")
                        self.animation2.setDuration(500)
                        self.animation2.setStartValue(150)
                        self.animation2.setEndValue(30)
                        self.animation2.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                        self.animation2.start()
                        self.Side_Menu_Num = 0


        def count(self):
                date1 = self.dateEdit_2.date().toPyDate()
                date2 = self.dateEdit_3.date().toPyDate()
                category = self.comboBox_2.currentText()
                res = self.Analis.sum_category_date(category, date1, date2)
                plt.bar(res['date'],res['price'])
                plt.show()

        def all_ctg(self):
                date1 = self.dateEdit_2.date().toPyDate()
                # date_1 = datetime.datetime.strptime(date1, "%Y-%m-%d")
                date2 = self.dateEdit_3.date().toPyDate()
                df = self.Analis.all_category_but_time(date1, date2)
                print(df)
                ctg = ['Інше','Їжа','Комунальні платежі','Підписки', 'Розваги','Шоппінг']
                plt.pie(df, labels=ctg, autopct='%1.1f%%')
                plt.show()



app = QApplication(sys.argv)
window = MainWindow_UI()
app.exec_()