# CS4400-Database-GUI
Final Project For Introduction To Database Systems
## Project Description
Given the base database schema, the task was to develop a set of database procedures and views for modification and display of the database contents within given parameters. \
In addition, a set of basic GUIs were created to allow user input without having to interact directly through MySQL
## Setup
First, run the datbase schema and procedure files in MySQL to initialize the database \
Then, for each instance of database "mysql.connector" in each of the files in the interface folder, replace user and password with corresponding information for own install \
Finally, run MainMenu.py
## Notes
On account of short timeframe and my lack of experience with pygui at the time the gui portion of this project was developed, the design focuses purely on being able to work over efficiency. Given a rewrite, a large portion of the code used in each file could be replaced with an abstract class to fix the large amount of reused code.
