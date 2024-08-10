from flask import Flask, render_template , request ,redirect , session
from product import productList
from cart import *
from order import *
from mysqlConn import *
from flask_session import Session


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


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

    query = ("SELECT * FROM proj_grocery_store.user WHERE user_email = %s AND user_pass = %s")

    mycursor.execute(query , (user_email ,user_pass))

    try :
        user_id = mycursor.fetchall()[0][0]
    except :
        msg =  "No user exists with this username and password."
        cnn.close()
        return render_template("login.html" , msg = msg)

    cnn.close()

    # create a session for the user with user_id
    session['user_id'] = user_id

    # return "Welcome to our website."
    return redirect("/home")






## code for registration part
@app.route('/register' , methods = ['POST'])
def register():
    user_name = request.form['username']
    user_email = request.form['useremail']
    user_pass = request.form['userpass']
    user_ph = request.form['userphnum']
    user_add = request.form['useraddr']

    # check it there is any null record ?
    if "" in [user_name , user_pass, user_email , user_ph , user_add] :
        return render_template("register.html" , msg = "Error ! Enter all the information correctly.")

    try:
        cnn = mysqlConnection()
        mycursor = cnn.cursor()
 
        mycursor.execute("INSERT INTO proj_grocery_store.user (user_name , user_pass, user_email , user_ph , user_add) VALUES(%s , %s , %s , %s , %s)" , (user_name , user_pass, user_email , user_ph , user_add))
        cnn.commit()
        cnn.close()

    except Exception as e:
        return f"{e}"

    return render_template("login.html")



## also define logout functionality
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')




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
@app.route('/addItem' , methods = ['post'])
def addItemtoCart():
    # id = request.args.get("id")
    prod_id = request.form['id']
    prod_qty = request.form['qty']

    addCartItems(prod_id , prod_qty)
    return redirect('/product')


## route for orders page
@app.route('/order')
def OrderPage():
    cartitems = cartItemList()
    totalPrice = totalOrderPrice()
    return render_template("orderDetails.html" , cartitems = cartitems , totalPrice = totalPrice)


## route for remove a cart item
@app.route('/removeItem')
def removeItemFromCart():
    id = request.args.get("id")
    removeCartItem(id)
    return redirect('/order')


## route for final order details
@app.route('/orderDetails' , methods = ['POST'])
def finalOrderDetails():
    # user_email = request.form['email']
    user_id = session['user_id']

    # createOrderDetails(user_email)
    createOrderDetails(user_id)

    # getting order details to display on final order details page
    finalOrdDetail = orderDetails(user_id)

    # making cart empty for that user_id
    cleanCart(user_id)

    return render_template("invoice.html", finalOrdDetail = finalOrdDetail)







if __name__ == '__main__':
    app.run(host='0.0.0.0' , debug=True)