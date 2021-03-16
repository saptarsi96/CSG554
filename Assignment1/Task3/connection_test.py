import mysql.connector
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="very_strong_password",
    auth_plugin="mysql_native_password"

)
# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor()
# executing cursor with execute method and pass SQL query
db_cursor.execute("CREATE DATABASE my_first_db")
# get list of all databases
db_cursor.execute("SHOW DATABASES")
# print all databases
for db in db_cursor:
    print(db)
