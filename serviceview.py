# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serviceview.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from distutils.util import execute
import sys
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableView, QTableWidgetItem, QHeaderView)
import mysql.connector 


class ServiceView(object):
    def ShowTable(self):
            cnx = mysql.connector.connect(user='root', password='(placeholder)',
                              host='127.0.0.1',
                              database='restaurant_supply_express', port=3306)
            mycursor = cnx.cursor()
            mycursor.execute("SELECT * FROM restaurant_supply_express.display_service_view;")
            myresult = mycursor.fetchall()
            self.tableWidget.setRowCount(0)

            for row_number, row_data in enumerate(myresult):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            cnx.close()
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(978, 604)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 281, 61))
        self.label.setObjectName("label")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(20, 110, 931, 341))
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.tableButton = QtWidgets.QPushButton(Form)
        self.tableButton.setGeometry(QtCore.QRect(420, 480, 151, 91))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tableButton.setFont(font)
        self.tableButton.setObjectName("tableButton")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableButton.clicked.connect(self.ShowTable)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:24pt;\">Service View</span></p></body></html>"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Long Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Home Base"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Manager"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Total Sales"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "# of Different Ingredients"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Total Product Cost"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Total Product Weight"))
        self.tableButton.setText(_translate("Form", "Show View"))

        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = ServiceView()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
