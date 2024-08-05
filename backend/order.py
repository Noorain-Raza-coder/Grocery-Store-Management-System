from datetime import datetime
from mysqlConn import mysqlConnection


def createOrderDetails(user_email):
    """This function insert the details into orders table."""

    # following is the order details
    #(order_id , order_date , customer_name , total_price) # order_id is auto increment so don't pass
    # lets collect it one by one.

    order_date = datetime.now()

    
    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    # fetching the total price of the product
    queryPrice = "SELECT SUM(prod_totalPrice) FROM grocery_store.cart"
    mycursor.execute(queryPrice)

    total_price = mycursor.fetchall()[0]

    # fetching user_name from the user table.
    queryUser = ("SELECT user_name FROM grocery_store.user WHERE user_email = %s")
    mycursor.execute(queryUser , (user_email,))

    user_name = mycursor.fetchall()[0]



    # inserting details into orders table
    customer_name = user_name[0]
    total_price = total_price[0]

    query = ("INSERT INTO grocery_store.orders (order_date , customer_name , total_price) VALUES (%s , %s , %s)")
    data = (order_date , customer_name , total_price)

    mycursor.execute(query , data)

    cnn.commit()

    cnn.close()

    return "details added successfully."
    




## add one more column into orders table i.e user_id so that you can fetch user data for invoice
## function that returns the order details from the orders table
def orderDetails():
    """This function returns a list of dictionary of order details.
    ex - """
    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = ("SELECT * FROM grocery_store.orders")
    mycursor.execute(query)

    order_detail_list = []
    for (order_id , order_date , customer_name , total_price) in mycursor.fetchall():
        order_detail_list.append(
            {
                "order_id" : order_id , "order_date" : order_date , "customer_name" : customer_name , "total_price" : total_price
            }
        )


    cnn.close()

    return order_detail_list





## function that return the invoice by fetching the results from orders and user table
def creatInvoice(order_id):
    """This function creates and return invoice in a json format."""

    # {"Order Id" : order_id , "User ID" : user_id , "Order Date" : order_date , Name : costomer_name , Ph Number :  , Email : , Address : , Total Price : total_price}

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query1 = ("SELECT * FROM grocery_store.orders WHERE order_id = %s")
    mycursor.execute(query1 , (order_id,))

    for (order_id , order_date, costomer_name , total_price) in mycursor.fetchall():
        order_id = order_id
        order_date = order_date
        costomer_name = costomer_name
        total_price = total_price

    # you also have to add user_id into orders table so that you can fetch user data. RNow you can assume user id 
    user_id = 1
    query2 = ("SELECT * FROM grocery_store.user WHERE user_id = %s")
    mycursor.execute(query2 , (user_id,))

    for (user_id , user_name , user_email , user_PhNum , user_addr) in mycursor.fetchall():
        user_id = user_id
        user_name = user_name
        user_email = user_email
        user_PhNum = user_PhNum
        user_addr = user_addr



    cnn.close()

    invoice = {
        "Order ID" : order_id,
        "User ID" : user_id ,
        "Order Date" : order_date ,
        "Name" : costomer_name,
        "Ph Number" : user_PhNum ,
        "Email" : user_email ,
        "Address" : user_addr ,
        "Total Price" : total_price
    }

    return invoice




if __name__ == '__main__':
    print(creatInvoice(1))