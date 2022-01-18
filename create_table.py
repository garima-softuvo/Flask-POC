import sqlite3

conn = sqlite3.connect("dbtable.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE Employees(
    id integer PRIMARY KEY,
    name text NOT NULL,
    salary float NOT NULL)"""
cursor.execute(sql_query)

# table2 = """ CREATE TABLE IF NOT EXISTS Details(
#     userid integer PRIMARY KEY,
#     company text NOT NULL,
#     year(s) float NOT NULL,
#     FOREIGN KEY (userid) REFERENCES Employees (id))"""
# cursor.execute(table2)



