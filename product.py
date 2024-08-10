from mysqlConn import mysqlConnection



## Function to show products
def productList():
    """This function returns a list of products dictionary.
    ex - [{'prod_id': 1, 'prod_name': 'Biscuit', 'prod_uom': 'each', 'prod_price': 10.0}]"""

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = "SELECT * FROM proj_grocery_store.product"
    mycursor.execute(query)

    productsList = []
    for (prod_id , prod_name , prod_uom , prod_price) in mycursor.fetchall():
        productsList.append(
            {
                "prod_id" : prod_id, 
                "prod_name" : prod_name, 
                "prod_uom" : prod_uom, 
                "prod_price" : prod_price
            }
        )

    cnn.close()
    return productsList

   
    
## this is pending task.
## fucntion that add product into product table, only can be done by website admin.
def addProduct(data):
    """ This function takes product's data as a dictionary and add the product into products table and returns none.
    ex- data = {"prod_name" : "Tomato" , "prod_uom" : "kg" , "prod_price" : 30} """

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = ("INSERT INTO proj_grocery_store.products ( prod_name , prod_uom , prod_price) "
            " VALUES ( %s , %s , %s) ")                                                       # (8 , 'Tomato' , ''kg'' , 30) , prod_id is auto_increment so don't need to pass

    data = (data["prod_name"] , data["prod_uom"] , data["prod_price"])

    mycursor.execute(query , data)

    cnn.commit()
    cnn.close()




## function that remove product from the cart table
def removeProduct(prod_id):
    """This function takes the product_id and remove it from the product table."""

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = (f"DELETE FROM grocery_store.products WHERE prod_id = {prod_id}")

    mycursor.execute(query)

    cnn.commit()
    cnn.close()



