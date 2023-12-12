#!/usr/bin/python3

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from Credentials import SECRETKEY
from sqlalchemy import func

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRETKEY

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///users.db")
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


############  models  ################
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    orders = db.relationship('Order', backref='user', cascade="all, delete-orphan", lazy=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.Integer, db.ForeignKey('user.email'), nullable=False)


with app.app_context():
    db.create_all()

################################

@app.route('/', strict_slashes=False)
def home_page():
    if current_user.is_authenticated:
        return render_template("index.html", name=current_user.name, logged_in=current_user.is_authenticated)

    return render_template("index.html")


@app.route("/about/", strict_slashes=False)
def about():
    if current_user.is_authenticated:
        return render_template("about.html", name=current_user.name, logged_in=current_user.is_authenticated)
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"], strict_slashes=False)
def register():
    if request.method == "POST":
        if request.form.get('password') != request.form.get('passconfirm'):
            flash("Passwords do not match. Please try again!", 'error')
            return redirect(url_for('register'))

        email = request.form.get('email')
        email_lower = email.lower()
        result = db.session.execute(db.select(User).where(func.lower(User.email) == email_lower))

        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!", 'warning')
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            password=hash_and_salted_password,
            name=request.form.get('name'),
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('profile', user_id=new_user.id))
       # return redirect(url_for("profile"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"], strict_slashes=False)
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        email_lower = email.lower()
        result = db.session.execute(db.select(User).where(func.lower(User.email) == email_lower))
        user = result.scalar()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.", 'error')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.', 'error')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('profile', user_id=user.id))

    return render_template("login.html", logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route('/profile/<int:user_id>', methods=["GET", "POST"], strict_slashes=False)
@login_required
def profile(user_id):
    email = current_user.email
    stocks = db.session.query(Order.id, Order.stock, Order.company).filter(Order.user_email == email).order_by(Order.stock).all()

    if request.method == "POST":
        new_stock = request.form.get('stock')
        new_company = request.form.get('company')

        result = db.session.execute(db.select(Order).where(
            (Order.user_email == email) &
            (Order.stock == new_stock) &
            (Order.company == new_company)
        ))

        order = result.scalar()
        if order:
            # Order already exists
            flash("You are already following this stock!", 'warning')
            return redirect(url_for('profile', user_id=user_id))

        new_order = Order(
            stock=new_stock,
            company=new_company,
            user_email=email,
        )
        db.session.add(new_order)
        db.session.commit()
        flash("New stock added successfully!", 'success')
        return redirect(url_for('profile', user_id=current_user.id, stocks=stocks))

    return render_template("profile.html", name=current_user.name, logged_in=True, stocks=stocks)


@app.route("/delete")
def delete_stock():
    stocks = request.args.get("orders")
    stock_id = request.args.get("id")
    stock = db.get_or_404(Order, stock_id)
    db.session.delete(stock)
    db.session.commit()
    return redirect(url_for('profile', user_id=current_user.id, stocks=stocks))


if __name__ == '__main__':
    app.run(debug=True)
