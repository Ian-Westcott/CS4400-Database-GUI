# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StartFunding.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableView, QTableWidgetItem)
import mysql.connector

class Start_Funding(object):
    def setupOwner(self):
        cnx = mysql.connector.connect(user='root', password='(placeholder)',
                              host='127.0.0.1',
                              database='restaurant_supply_express', port=3306)
        mycursor = cnx.cursor()
        mycursor.execute("select username from restaurant_owners")
        myresult = mycursor.fetchall()
        for row_data in myresult:
            for data in row_data:
                self.Owner.addItem(data)
        cnx.close
    
    def setupRestaurant(self):
        cnx = mysql.connector.connect(user='root', password='Fl1ght413612!',
                              host='127.0.0.1',
                              database='restaurant_supply_express', port=3306)
        mycursor = cnx.cursor()
        mycursor.execute("select long_name from restaurants")
        myresult = mycursor.fetchall()
        for row_data in myresult:
            for data in row_data:
                self.RestaurantName.addItem(data)
        cnx.close

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(576, 332)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(130, -30, 321, 151))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.StartFunding = QtWidgets.QPushButton(Form)
        self.StartFunding.setGeometry(QtCore.QRect(200, 260, 191, 28))
        self.StartFunding.setObjectName("StartFunding")
        self.Owner = QtWidgets.QComboBox(Form)
        self.Owner.setGeometry(QtCore.QRect(100, 90, 401, 22))
        self.Owner.setObjectName("Owner")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 61, 31))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(30, 140, 71, 41))
        self.label_4.setObjectName("label_4")
        self.RestaurantName = QtWidgets.QComboBox(Form)
        self.RestaurantName.setGeometry(QtCore.QRect(100, 150, 401, 22))
        self.RestaurantName.setObjectName("RestaurantName")
        self.setupOwner()
        self.setupRestaurant()
        self.StartFunding.clicked.connect(self.fundRestaurant)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Change Restaurant Owner"))
        self.StartFunding.setText(_translate("Form", "Change Restaurant Owner"))
        self.label_2.setText(_translate("Form", "Owner \n"
"Username"))
        self.label_4.setText(_translate("Form", "Name of \n"
"Restaurant"))

    def fundRestaurant(self):
        cnx = mysql.connector.connect(user='root', password='Fl1ght413612!',
                      host='127.0.0.1',
                      database='restaurant_supply_express', port=3306)
        cursor = cnx.cursor()
        cursor.callproc('start_funding', [self.Owner.currentText(), self.RestaurantName.currentText()])
        cnx.commit()
        cnx.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Start_Funding()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
