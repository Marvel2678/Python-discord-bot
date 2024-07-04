import mysql.connector
def connectToDatabase():
    connection = mysql.connector.connect(
        host="localhost",
        user='root',
        password='',
        database='maturaBot'
    )
    return connection
