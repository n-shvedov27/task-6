from flask import jsonify, request, url_for, render_template, redirect, flash

from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from typing import List
from multiprocessing import Process
from time import sleep
import random

from server.wsgi import app
from .models import db, Currency, Client, Purchase
from .forms import LoginForm, RegistrationForm

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)  # set up login manager


@login_manager.user_loader
def load_user(user_id):
    return Client.query.get(int(user_id))  # returns User object or None


@app.route('/')
def index():
    currencies = Currency.query.order_by(Currency.currency_name).all()

    return render_template('index.html', currencies=currencies)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        client_name = form.client_name.data
        password = form.password.data
        client = Client.query.filter_by(client_name=client_name).first()
        if client is not None and client.verify_password(password):
            login_user(client)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')

    return render_template('login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit() or app.config['TESTING']:
        username = form.client_name.data
        password = form.password.data
        user = Client(client_name=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create_currency', methods=["POST"])
def create_currency():
    currency_name = request.form.get('currency_name', None)
    cost = request.form.get('cost', None)
    if not currency_name or not cost:
        return "Not enough data"
    currency = Currency(currency_name, cost)
    db.session.add(currency)
    db.session.commit()
    return "Sucses"


@app.route('/create_purchase/<currency_id>', methods=["GET"])
def create_purchase(currency_id):
    current_user.make_purchase(int(currency_id), 1)

    return redirect(url_for('index'))


@app.template_filter('get_count_clients_purchases')
def get_count_clients_purchases(purchases: List[Purchase]):
    copy = []
    for purchase in purchases:
        if purchase.client_id == current_user.id:
            copy.append(purchase)
    return len(copy)


@app.route('/get_currency', methods=["GET"])
def get_currencies_info():
    currencies = Currency.query.order_by(Currency.currency_name).all()

    return jsonify({'data': render_template('currencies.html', currencies=currencies)})


def update_currency_cost():
    while True:
        sleep(1)
        currencies = Currency.query.all()
        for currency in currencies:
            currency.cost = currency.cost + random.randint(-10, 10)
        db.session.commit()


update_currency_process = Process(target=update_currency_cost)

update_currency_process.start()
