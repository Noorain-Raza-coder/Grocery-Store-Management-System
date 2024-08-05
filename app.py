from flask import Flask, render_template , request ,redirect
from product import productList
from cart import *


app = Flask(__name__)

## route for home page
@app.route('/')
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
    return render_template("orderDetails.html" , cartitems = cartitems)



## route for remove a cart item
@app.route('/removeItem')
def removeItemFromCart():
    id = request.args.get("id")
    removeCartItem(id)
    return redirect('/order')







if __name__ == '__main__':
    app.run(host='0.0.0.0' , debug=True)