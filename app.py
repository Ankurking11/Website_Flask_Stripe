from flask import Flask, render_template, redirect, flash, url_for, request, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import razorpay
import logging
import razorpay

# Initialize Flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:adminpass@localhost/demo1'
db = SQLAlchemy(app)
app.app_context().push()
app.config['SECRET_KEY'] = 'PAYMENT_APP'

#user table
class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

#product table
class Product(db.Model):
    __tablename__='product'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False)
    descr = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

#transaction table
class Transaction(db.Model):
    __tablename__='transaction'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
    product = db.relationship('Product', backref=db.backref('transactions', lazy=True))

@app.route('/')
def index():
    return render_template('index.html')

#register
@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        products = Product.query.all()
        return render_template('product.html', products=products)
    
    return render_template('register.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if password == user.password:
            session['user_id'] = user.id
            flash('Login Successful')
            products = Product.query.all()
            return render_template('product.html', products=products)
        else:
            flash('Invalid email or password')
    return render_template('login.html')


#buy
@app.route('/buy/<int:product_id>', methods=['GET', 'POST'])
def buy(product_id):
    if request.method == 'POST':
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        product = Product.query.filter_by(id=product_id).first()
        amount = product.price*100
        client = razorpay.Client(auth = ("rzp_test_I9GZQqSmWyMm0h" , "Ft34wtwLr0olMmEaK0GV5vJb"))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

        return render_template('checkout.html',user=user,product=product, amount = amount, payment = payment)
    return render_template('buy.html')


#success
@app.route('/success/<order_id>/<product_id>', methods=['GET','POST'])
def success(order_id,product_id):
    order_id = order_id
    prod_id = product_id
    user_id = session['user_id']
    client = razorpay.Client(auth = ("rzp_test_I9GZQqSmWyMm0h" , "Ft34wtwLr0olMmEaK0GV5vJb"))
    order_details = client.order.payments(order_id)
    transaction_id = order_details['items'][-1]['id']
    amount = order_details['items'][-1]['amount']/100
    status = order_details['items'][-1]['status']

    transaction = Transaction(product_id=prod_id, user_id=user_id, 
                              transaction_id=transaction_id, 
                              amount=amount)
    db.session.add(transaction)
    db.session.commit()

    return render_template("success.html",transaction_id=transaction_id, 
                           amount=amount,status=status)


if __name__ == '__main__':
    app.run(debug=True)