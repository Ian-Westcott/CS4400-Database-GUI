# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RemovePilot.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableView, QTableWidgetItem)
import mysql.connector

class Remove_Pilot_Role(object):
    def setupPilots(self):
        cnx = mysql.connector.connect(user='root', password='(placeholder)',
                              host='127.0.0.1',
                              database='restaurant_supply_express', port=3306)
        mycursor = cnx.cursor()
        mycursor.execute("select username from pilots where username not in (select flown_by from drones where flown_by is not null);")
        myresult = mycursor.fetchall()
        for row_data in myresult:
            for data in row_data:
                self.PilotUsername.addItem(data)
        cnx.close

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(576, 224)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(170, -30, 341, 131))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.removeDroneButton = QtWidgets.QPushButton(Form)
        self.removeDroneButton.setGeometry(QtCore.QRect(210, 160, 121, 28))
        self.removeDroneButton.setObjectName("removeDroneButton")
        self.PilotUsername = QtWidgets.QComboBox(Form)
        self.PilotUsername.setGeometry(QtCore.QRect(90, 80, 401, 22))
        self.PilotUsername.setObjectName("PilotUsername")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 61, 31))
        self.label_2.setObjectName("label_2")
        self.setupPilots()
        self.removeDroneButton.clicked.connect(self.removePilot)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Remove Pilot Role"))
        self.removeDroneButton.setText(_translate("Form", "Remove Pilot"))
        self.label_2.setText(_translate("Form", "Pilot\n"
"Username"))

    def removePilot(self):
        if (len(self.PilotUsername.currentText()) > 0):
            cnx = mysql.connector.connect(user='root', password='Fl1ght413612!',
                          host='127.0.0.1',
                          database='restaurant_supply_express', port=3306)
            cursor = cnx.cursor()
            cursor.callproc('remove_pilot_role', [self.PilotUsername.currentText()])
            cnx.commit()
            cnx.close()
            self.PilotUsername.clear()
            self.setupPilots()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Remove_Pilot_Role()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())