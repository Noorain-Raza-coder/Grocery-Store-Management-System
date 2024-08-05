from flask import Flask, render_template , request ,redirect
from product import productList
from cart import *
from order import *


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