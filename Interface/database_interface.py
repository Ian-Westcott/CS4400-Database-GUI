from distutils.util import execute
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTableView)
import mysql.connector 

Form, Window = uic.loadUiType("employeeview.ui")
cnx = mysql.connector.connect(user='root', password='(placeholder)',
                              host='127.0.0.1',
                              database='restaurant_supply_express', port=3306)
mycursor = cnx.cursor()
mycursor.execute("select employees.username, taxID, salary, hired, employees.experience as employee_experience,  ifnull(licenseID, 'n/a') , ifnull(pilots.experience, 'n/a') as successful_flights, CASE when (employees.username in (select manager from delivery_services)) then 'yes' else 'no' end as manager from employees left outer join pilots on employees.username = pilots.username;;")
myresult = mycursor.fetchall()
for row_number, row_data in myresult:
    
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec()



# Your application won't reach here until you exit and the event
# loop has stopped.