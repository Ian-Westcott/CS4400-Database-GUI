# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'JoinSwarm.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableView, QTableWidgetItem)
import mysql.connector

class Join_Swarm(object):
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
        mycursor.execute("select tag from drones where id = \'"+ self.DroneID.currentText() + "\' and flown_by is not null and tag not in (select swarm_tag from drones where flown_by is null and swarm_id = \'"+ self.DroneID.currentText() + "\');")
        myresult = mycursor.fetchall()
        for row_data in myresult:
            for data in row_data:
                self.DroneTag.addItem(str(data))
        cnx.close()

    def setupLeaderTag(self):
        cnx = mysql.connector.connect(user='root', password='Fl1ght413612!',
                              host='127.0.0.1',
                              database='restaurant_supply_express', port=3306)
        mycursor = cnx.cursor()
        mycursor.execute("select tag from drones where (id = \'"+ self.DroneID.currentText() + "\' and flown_by is not null and tag != \'"+ self.DroneTag.currentText() +"\' and hover = (select hover from drones where id = \'"+ self.DroneID.currentText() + "\' and tag = \'"+ self.DroneTag.currentText() +"\'));")
        myresult = mycursor.fetchall()
        for row_data in myresult:
            for data in row_data:
                self.LeaderTag.addItem(str(data))
        cnx.close()

    def DroneIDChange(self):
        self.DroneTag.clear()
        self.LeaderTag.clear()
        self.setupDroneTag()
        self.setupLeaderTag()

    def DroneTagChange(self):
        self.LeaderTag.clear()
        self.setupLeaderTag()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(576, 332)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(150, -40, 261, 131))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 170, 81, 51))
        self.label_6.setObjectName("label_6")
        self.joinSwarmButton = QtWidgets.QPushButton(Form)
        self.joinSwarmButton.setGeometry(QtCore.QRect(220, 260, 121, 28))
        self.joinSwarmButton.setObjectName("joinSwarmButton")
        self.LeaderTag = QtWidgets.QComboBox(Form)
        self.LeaderTag.setGeometry(QtCore.QRect(90, 190, 401, 22))
        self.LeaderTag.setObjectName("LeaderTag")
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
        self.setupDroneID()
        self.setupDroneTag()
        self.setupLeaderTag()
        self.DroneID.currentIndexChanged.connect(self.DroneIDChange)
        self.DroneTag.currentIndexChanged.connect(self.DroneTagChange)
        self.joinSwarmButton.clicked.connect(self.joinSwarm)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Add Drone To Swarm"))
        self.label_6.setText(_translate("Form", "Leader Drone\n"
"Tag"))
        self.joinSwarmButton.setText(_translate("Form", "Join Swarm"))
        self.label_2.setText(_translate("Form", "Drone ID"))
        self.label_4.setText(_translate("Form", "Drone Tag"))

    def joinSwarm(self):
        cnx = mysql.connector.connect(user='root', password='Fl1ght413612!',
                          host='127.0.0.1',
                          database='restaurant_supply_express', port=3306)
        cursor = cnx.cursor()
        cursor.callproc('join_swarm', [self.DroneID.currentText(), self.DroneTag.currentText(), self.LeaderTag.currentText()])
        cnx.commit()
        cnx.close()
        self.DroneIDChange()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Join_Swarm()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
