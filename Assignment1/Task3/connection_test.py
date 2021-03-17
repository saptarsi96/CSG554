import mysql.connector
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="very_strong_password",
    auth_plugin="mysql_native_password"

)

while(True):
    print("-------------------------------TERMINAL-----------------------------------")
    query = input()
    db_cursor = db_connection.cursor()
    db_cursor.execute("use test")
    try:
        db_cursor.execute(query)
        for db in db_cursor:
            print(db)
    except:
        print("There is syntax error in your sql command!")
        continue
        






