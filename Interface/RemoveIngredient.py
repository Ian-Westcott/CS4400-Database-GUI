# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RemoveIngredient.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableView, QTableWidgetItem)
import mysql.connector

class Remove_Ingredient(object):
    def setupBarcode(self):
        cnx = mysql.connector.connect(user='root', password='(placeholder)',
                              host='127.0.0.1',
                              database='restaurant_supply_express', port=3306)
        mycursor = cnx.cursor()
        mycursor.execute("select barcode from ingredients where barcode not in (select barcode from payload)")
        myresult = mycursor.fetchall()
        for row_data in myresult:
            for data in row_data:
                self.Barcode.addItem(data)
        cnx.close()
        mycursor.close()
        
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(576, 251)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(170, -30, 261, 131))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.removeIngredientButton = QtWidgets.QPushButton(Form)
        self.removeIngredientButton.setGeometry(QtCore.QRect(210, 170, 131, 28))
        self.removeIngredientButton.setObjectName("removeIngredientButton")
        self.Barcode = QtWidgets.QComboBox(Form)
        self.Barcode.setGeometry(QtCore.QRect(90, 90, 401, 22))
        self.Barcode.setObjectName("Barcode")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 61, 31))
        self.label_2.setObjectName("label_2")
        self.setupBarcode()
        self.removeIngredientButton.clicked.connect(self.removeIngredient)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Remove Ingredient"))
        self.removeIngredientButton.setText(_translate("Form", "Remove Ingredient"))
        self.label_2.setText(_translate("Form", "Ingredient\n"
"Barcode"))

    def removeIngredient(self):
        if (len(self.Barcode.currentText()) > 0):
            cnx = mysql.connector.connect(user='root', password='Fl1ght413612!',
                          host='127.0.0.1',
                          database='restaurant_supply_express', port=3306)
            cursor = cnx.cursor()
            cursor.callproc('remove_ingredient', [self.Barcode.currentText()])
            cnx.commit()
            cnx.close()
            self.Barcode.clear()
            self.setupBarcode()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Remove_Ingredient()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
