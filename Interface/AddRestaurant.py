# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddRestaurant.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableView, QTableWidgetItem)
import mysql.connector

class Add_Restaurant(object):
    def setupDropDown(self):
        cnx = mysql.connector.connect(user='root', password='(placeholder)',
                              host='127.0.0.1',
                              database='restaurant_supply_express', port=3306)
        mycursor = cnx.cursor()
        mycursor.execute("select label from locations;")
        myresult = mycursor.fetchall()
        for row_data in myresult:
            for data in row_data:
                self.Location.addItem(data)
        cnx.close()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(576, 378)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(190, -30, 211, 131))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 71, 21))
        self.label_3.setObjectName("label_3")
        self.NameEntry = QtWidgets.QLineEdit(Form)
        self.NameEntry.setGeometry(QtCore.QRect(100, 130, 401, 22))
        self.NameEntry.setText("")
        self.NameEntry.setObjectName("NameEntry")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(30, 170, 71, 31))
        self.label_5.setObjectName("label_5")
        self.RatingEntry = QtWidgets.QLineEdit(Form)
        self.RatingEntry.setGeometry(QtCore.QRect(100, 180, 401, 22))
        self.RatingEntry.setObjectName("RatingEntry")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(30, 70, 61, 31))
        self.label_6.setObjectName("label_6")
        self.addRestaurant = QtWidgets.QPushButton(Form)
        self.addRestaurant.setGeometry(QtCore.QRect(230, 310, 101, 28))
        self.addRestaurant.setObjectName("addRestaurant")
        self.Location = QtWidgets.QComboBox(Form)
        self.Location.setGeometry(QtCore.QRect(100, 80, 401, 22))
        self.Location.setObjectName("Location")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 220, 81, 31))
        self.label_2.setObjectName("label_2")
        self.SpentEntry = QtWidgets.QLineEdit(Form)
        self.SpentEntry.setGeometry(QtCore.QRect(100, 230, 401, 22))
        self.SpentEntry.setObjectName("SpentEntry")
        self.setupDropDown()
        self.SpentEntry.setValidator(QIntValidator())
        self.RatingEntry.setValidator(QIntValidator())
        self.addRestaurant.clicked.connect(self.addnewRestaurant)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Add a Restaurant"))
        self.label_3.setText(_translate("Form", "Name"))
        self.label_5.setText(_translate("Form", "Rating"))
        self.label_6.setText(_translate("Form", "Location"))
        self.addRestaurant.setText(_translate("Form", "Add Restaurant"))
        self.label_2.setText(_translate("Form", "Money Spent"))

    def addnewRestaurant(self):
        if (len(self.NameEntry.text()) > 0 and len(self.NameEntry.text()) <= 40 and len(self.RatingEntry.text()) > 0 and len(self.SpentEntry.text()) > 0):
            cnx = mysql.connector.connect(user='root', password='Fl1ght413612!',
                          host='127.0.0.1',
                          database='restaurant_supply_express', port=3306)
            cursor = cnx.cursor()
            cursor.callproc('add_restaurant', [self.NameEntry.text(), self.RatingEntry.text(), self.SpentEntry.text(), self.Location.currentText()])
            cnx.commit()
            cnx.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Add_Restaurant()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())