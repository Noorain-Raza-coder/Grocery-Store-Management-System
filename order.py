from mysqlConn import mysqlConnection




## get total price of the order
def totalOrderPrice():
    """This function return the total price of the cart items/values."""

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    # fetching the total price of the product
    queryPrice = "SELECT SUM(prod_tot_price) FROM proj_grocery_store.cart"
    mycursor.execute(queryPrice)

    total_price = mycursor.fetchall()[0][0]

    cnn.close()
    return total_price




def createOrderDetails(user_id):
    """This function insert the details into orders table."""

    total_price = totalOrderPrice()
    print(total_price)
    print(user_id)

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = "INSERT INTO proj_grocery_store.order (user_id, total_price) VALUES (%s, %s)"
    data = (user_id, total_price)

    mycursor.execute(query, data)
    cnn.commit()
    cnn.close()

    return "details added successfully."
    




## add one more column into orders table i.e user_id so that you can fetch user data for invoice
## function that returns the order details from the orders table
def orderDetails(user_id):
    """This function returns a list of dictionary of order details.
    ex - """
    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = ("SELECT t1.order_id , t1.user_id , t2.user_name, t2.user_email ,t2.user_ph , t2.user_add , t1.total_price "
                "FROM proj_grocery_store.order t1 "
                "JOIN proj_grocery_store.user t2 "
                "ON t1.user_id = t2.user_id "
                "WHERE t1.user_id = %s "
                "ORDER BY t1.order_id DESC "
                "LIMIT 1")

    # data = (user_id,user_id)
    mycursor.execute(query , (user_id,))

    order_detail_list = []
    for (order_id , user_id , user_name , user_email ,user_ph ,user_add, total_price) in mycursor.fetchall():
        order_detail_list.append(
            {
                "order_id" : order_id , "user_id" : user_id , "user_name" : user_name , "user_email" : user_email , "user_ph" : user_ph , "user_add" : user_add ,"total_price" : total_price
            }
        )

    cnn.close()
    return order_detail_list[0]

