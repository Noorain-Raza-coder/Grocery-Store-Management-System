from mysqlConn import mysqlConnection


## function that return list of cart items/products
def cartItemList():
    """This function returns a list of dictionary of cart items."""
    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = ("SELECT * FROM grocery_store.cart")
    mycursor.execute(query)

    cartItems = []

    for (prod_id , prod_name , prod_quantity , prod_totalPrice) in mycursor.fetchall():
        cartItems.append({
            "prod_id" : prod_id , 
            "prod_name" : prod_name , 
            "prod_quantity" : prod_quantity , 
            "prod_totalPrice" :  prod_totalPrice
        })

    cnn.close()

    return cartItems




## function that adds products into cart table
def addCartItems(prod_id , prod_quantity = 1):
    """This function takes a product id and adds that product into cart table."""

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = ("INSERT INTO grocery_store.cart (prod_id , prod_name , prod_quantity , prod_totalPrice) "
                "VALUES (%s , %s , %s , %s) ")

    prodQuery = (f"SELECT prod_name,prod_price FROM grocery_store.products WHERE prod_id = {prod_id}")
    mycursor.execute(prodQuery)

    # fetching the product anme and product price from product table for given product id.
    prod_data = []
    for (prod_name, prod_price) in mycursor.fetchall():
        prod_data.append({"prod_name"  : prod_name, "prod_price" : prod_price})

    prod_id = prod_id
    prod_name = prod_data[0]["prod_name"]
    prod_quantity = prod_quantity
    prod_totalPrice = prod_quantity * prod_data[0]["prod_price"]

    data = (prod_id , prod_name , prod_quantity , prod_totalPrice)

    mycursor.execute(query , data)

    cnn.commit()

    cnn.close()

    return "item added into cart successfully."





## 
def removeCartItem(prod_id):
    """This function takes item/product id and removes that item from the cart."""

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = (f"DELETE FROM grocery_store.cart WHERE prod_id = {prod_id}")
    mycursor.execute(query)

    cnn.commit()
    cnn.close()

    return "Item removed successfully."





















if __name__ == '__main__':
    print(removeCartItem(9))
    
    