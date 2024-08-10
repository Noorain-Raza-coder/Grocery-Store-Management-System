from mysqlConn import mysqlConnection
from flask_session import Session
from flask import session

## function that return list of cart items/products
def cartItemList():
    """This function returns a list of dictionary of cart items."""
    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    user_id = session['user_id']

    query = "SELECT * FROM proj_grocery_store.cart WHERE user_id = %s"
    mycursor.execute(query , (user_id,))

    cartItems = []

    for (cart_id , user_id , prod_id, prod_qty, prod_tot_price) in mycursor.fetchall():
        cartItems.append({
            "cart_id" : cart_id , 
            "user_id" : user_id , 
            "prod_id" : prod_id , 
            "prod_qty" :  prod_qty,
            "prod_tot_price": prod_tot_price
        })

    cnn.close()

    return cartItems




## function that adds products into cart table
def addCartItems(prod_id , prod_qty):
    """This function takes a product id and adds that product into cart table."""

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    # fetching product price
    prodQuery = "SELECT prod_price FROM proj_grocery_store.product WHERE prod_id = %s"
    mycursor.execute(prodQuery , (prod_id,))
    prod_price = mycursor.fetchall()[0][0]

    prod_tot_price = int(prod_qty) * prod_price

    # inserting items to cart
    mainquery = "INSERT INTO proj_grocery_store.cart (user_id , prod_id , prod_qty , prod_tot_price) VALUES (%s,%s,%s,%s)"
    
    user_id = session['user_id']
    data = (user_id , prod_id, prod_qty, prod_tot_price)

    mycursor.execute(mainquery,data)
    cnn.commit()
    cnn.close()

    return "item added into cart successfully."





## this function remove item from cart
def removeCartItem(prod_id):
    """This function takes item/product id and removes that item from the cart."""

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = (f"DELETE FROM proj_grocery_store.cart WHERE prod_id = {prod_id}")
    mycursor.execute(query)

    cnn.commit()
    cnn.close()

    return "Item removed successfully."



## making cart empty for given user_id
def cleanCart(user_id):
    """This function takes userid and removes all the item from the cart for that user id."""

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = (f"DELETE FROM proj_grocery_store.cart WHERE user_id = {user_id}")
    mycursor.execute(query)

    cnn.commit()
    cnn.close()

    return "cart is cleaned now."

    