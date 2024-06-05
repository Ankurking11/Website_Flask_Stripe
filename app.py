from flask import Flask, render_template, redirect, flash, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# from models import db, User, Product, Transaction
# from config import Config
#import razorpay

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "GeeksForGeeks"

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:adminpass@localhost/demo1'
db = SQLAlchemy(app)
app.app_context().push()

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
    desc = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)


#transaction table
class Transaction(db.Model):
    __tablename__='transaction'
    id = db.Column(db.Integer, primary_key=True)
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
        return redirect('login.html')

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if password == user.password:
            flash('Login Successful')
            return render_template('index.html')
        # if user and user.password:
        #     login_user(user)
        #     return redirect('index.html')
        else:
            flash('Invalid email or password')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)