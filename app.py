from flask import Flask, render_template , request ,redirect
from product import productList
from cart import *
from order import *
from mysqlConn import *


app = Flask(__name__)




@app.route('/')
def WelcomePage():
    return render_template("login.html")

@app.route('/createAccount')
def registrationPage():
    return render_template("register.html")


## code for login part
@app.route('/login' , methods = ['post'])
def login():
    user_email = request.form["useremail"]
    user_pass = request.form["userpass"]

    cnn = mysqlConnection()
    mycursor = cnn.cursor()

    query = ("SELECT * FROM grocery_store.user WHERE user_email = %s AND user_pass = %s")

    mycursor.execute(query , (user_email ,user_pass))

    if len(mycursor.fetchall()) == 0 :
        cnn.close()
        return render_template("login.html" , msg = "No user exists with this username and password.")

    cnn.close()
    # return "Welcome to our website."
    return redirect("/home")






## code for registration part
@app.route('/register' , methods = ['POST'])
def register():
    user_name = request.form['username']
    user_email = request.form['useremail']
    user_pass = request.form['userpass']
    user_PhNum = request.form['userphnum']
    user_addr = request.form['useraddr']

    # check it there is any null record ?
    if "" in [user_name , user_email , user_pass , user_PhNum , user_addr] :
        return render_template("register.html" , msg = "Error ! Enter all the information correctly.")

    try:
        cnn = mysqlConnection()
        mycursor = cnn.cursor()
 
        mycursor.execute("INSERT INTO grocery_store.user (user_name , user_email , user_pass , user_PhNum , user_addr) VALUES(%s , %s , %s , %s , %s)" , (user_name , user_email , user_pass , user_PhNum , user_addr))
        cnn.commit()
        cnn.close()

    except Exception as e:
        return f"{e}"

    return render_template("login.html")






## route for home page
@app.route('/home')
def HomePage():
    return render_template("home.html")


## route for shop page
@app.route('/product')
def ProductsPage():
    products = productList()
    return render_template("products.html" , products = products)


## route for add items to cart table
@app.route('/addItem')
def addItemtoCart():
    id = request.args.get("id")
    addCartItems(id)
    return redirect('/product')


## route for orders page
@app.route('/order')
def OrderPage():
    cartitems = cartItemList()
    totalPrice = totalOrderPrice()
    return render_template("orderDetails.html" , cartitems = cartitems , totalPrice = totalPrice[0])


## route for remove a cart item
@app.route('/removeItem')
def removeItemFromCart():
    id = request.args.get("id")
    removeCartItem(id)
    return redirect('/order')


## route for final order details
@app.route('/orderDetails' , methods = ['POST'])
def finalOrderDetails():
    user_email = request.form['email']
    createOrderDetails(user_email)

    # getting order details to display on final order details page
    finalOrdDetail = orderDetails()

    return render_template("finalOrderDetail.html", finalOrdDetail = finalOrdDetail)



## route to get the invoice
@app.route('/invoice/<order_id>', methods = ['POST'])
def invoice(order_id):
    yrInvoice = creatInvoice(order_id)
    return render_template("invoice.html" , yrInvoice = yrInvoice)




if __name__ == '__main__':
    app.run(host='0.0.0.0' , debug=True)