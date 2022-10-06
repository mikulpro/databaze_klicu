#!/bin/bash

python3 create_db.py

sqlite3 keys_test.db ".mode csv" -separator ";" ".import data/data_Titles.csv Titles" ".exit"
#sqlite3  -separator ";" -cmd ".import data/data_Borrowers.csv Borrowers" keys_test.db
#sqlite3  -separator ";" -cmd ".import data/data_BorrowersTitles.csv BorrowersTitles" keys_test.db
#sqlite3  -separator ";" -cmd ".import data/data_BorrowersWorkplaces.csv BorrowersWorkplaces" keys_test.db
#sqlite3  -separator ";" -cmd ".import data/data_Doorkeepers.csv Doorkeepers" keys_test.db
#sqlite3  -separator ";" -cmd ".import data/data_Faculties.csv Faculties" keys_test.db
#sqlite3  -separator ";" -cmd ".import data/data_Keys.csv Keys" keys_test.db
#sqlite3  -separator ";" -cmd ".import data/data_KeysRooms.csv KeysRooms" keys_test.db
#sqlite3  -separator ";" -cmd ".import data/data_Rooms.csv Rooms" keys_test.db
#sqlite3  -separator ";" -cmd ".import data/data_RoomTypes.csv RoomTypes" keys_test.db
#sqlite3  -separator ";" -cmd ".import data/data_Titles.csv Titles" keys_test.db
#sqlite3  -separator ";" -cmd ".import data/data_Workplaces.csv Workplaces" keys_test.db