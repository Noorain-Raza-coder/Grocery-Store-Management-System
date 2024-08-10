import mysql.connector


def mysqlConnection():
    ## create connection
    cnn = mysql.connector.connect(user = 'root' , password = 'Mysql$2002' , host = '127.0.0.1' , database = 'proj_grocery_store')

    try :
        if cnn :
            return cnn
    except Exception as e:
        print(e)


