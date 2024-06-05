from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager, login_user, login_required, logout_user, current_user
# # from models import db, User, Product, Transaction
# # from config import Config
# import razorpay

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:Sql@2000@localhost/demo1'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__='demo1'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

def __init__(self,id,name,email):
    self.id = id
    self.name = name
    self.email = email
    self.password = password


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST','GET'])
def register

if __name__ == '__main__':
    app.run(debug=True)