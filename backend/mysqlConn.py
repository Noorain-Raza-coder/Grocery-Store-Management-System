import mysql.connector


def mysqlConnection():

    cnn = mysql.connector.connect(host = '127.0.0.1' , user = 'root' , password = 'Mysql$2002' , database = 'grocery_store')

    return cnn

