# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RefuelDrone.ui'
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

class Refuel_Drone(object):
    def setupDroneID(self):
        cnx = mysql.connector.connect(user='root', password='(placeholder)',
                              host='127.0.0.1',
                              database='restaurant_supply_express', port=3306)
        mycursor = cnx.cursor()
        mycursor.execute("select distinct id from drones;")
        myresult = mycursor.fetchall()
        for row_data in myresult:
            for data in row_data:
                self.DroneID.addItem(data)
        cnx.close()

    def setupDroneTag(self):
        cnx = mysql.connector.connect(user='root', password='Fl1ght413612!',
                              host='127.0.0.1',
                              database='restaurant_supply_express', port=3306)
        mycursor = cnx.cursor()
        mycursor.execute("select tag from drones where id = \'"+ self.DroneID.currentText() + "\'")
        myresult = mycursor.fetchall()
        for row_data in myresult:
            for data in row_data:
                self.DroneTag.addItem(str(data))
        cnx.close()

    def DroneIDChange(self):
        self.DroneTag.clear()
        self.setupDroneTag()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(576, 307)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(210, -30, 261, 131))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.RefuelDroneButton = QtWidgets.QPushButton(Form)
        self.RefuelDroneButton.setGeometry(QtCore.QRect(210, 260, 121, 28))
        self.RefuelDroneButton.setObjectName("RefuelDroneButton")
        self.DroneID = QtWidgets.QComboBox(Form)
        self.DroneID.setGeometry(QtCore.QRect(90, 70, 401, 22))
        self.DroneID.setObjectName("DroneID")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 55, 16))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 130, 61, 16))
        self.label_4.setObjectName("label_4")
        self.DroneTag = QtWidgets.QComboBox(Form)
        self.DroneTag.setGeometry(QtCore.QRect(90, 130, 401, 22))
        self.DroneTag.setObjectName("DroneTag")
        self.FuelEntry = QtWidgets.QLineEdit(Form)
        self.FuelEntry.setGeometry(QtCore.QRect(90, 190, 401, 22))
        self.FuelEntry.setObjectName("FuelEntry")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20, 180, 81, 41))
        self.label_3.setObjectName("label_3")
        self.setupDroneID()
        self.setupDroneTag()
        self.DroneID.currentIndexChanged.connect(self.DroneIDChange)
        self.RefuelDroneButton.clicked.connect(self.refuelDrone)
        self.FuelEntry.setValidator(QIntValidator())

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Refuel Drone"))
        self.RefuelDroneButton.setText(_translate("Form", "Refuel Drone"))
        self.label_2.setText(_translate("Form", "Drone ID"))
        self.label_4.setText(_translate("Form", "Drone Tag"))
        self.label_3.setText(_translate("Form", "Fuel to\n"
"Add"))

    def refuelDrone(self):
        if (len(self.FuelEntry.text()) > 0):
            cnx = mysql.connector.connect(user='root', password='Fl1ght413612!',
                          host='127.0.0.1',
                          database='restaurant_supply_express', port=3306)
            cursor = cnx.cursor()
            cursor.callproc('refuel_drone', [self.DroneID.currentText(), self.DroneTag.currentText(), self.FuelEntry.text()])
            cnx.commit()
            cnx.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Refuel_Drone()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
