from flask_sqlalchemy import SQLAlchemy
from .wsgi import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy(app)


class Purchase(db.Model):
    def __init__(self, count: int, currency_id: int, client_id: int):
        self.count = count
        self.currency_id = currency_id
        self.client_id = client_id

    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    currency = db.relationship('Currency', back_populates="purchases")
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', back_populates='purchases')



class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_name = db.Column(db.String(120), unique=True)
    cost = db.Column(db.Float, nullable=False)
    purchases = db.relationship('Purchase', back_populates="currency")

    def __init__(self, currency_name: str, cost: str):
        self.currency_name = currency_name
        self.cost = cost


class Client(UserMixin, db.Model):
    def __init__(self, client_name: str, password: str):
        self.client_name = client_name
        self.password_hash = generate_password_hash(password)

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    purchases = db.relationship('Purchase', back_populates="client")

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def make_purchase(self, currency_id: int, count: int):
        currency = Currency.query.get(currency_id)
        if currency:
            purchase = Purchase(count, currency_id, self.id)

            currency.purchases.append(purchase)
            purchase.currency = currency

            self.purchases.append(purchase)
            purchase.client = self

            db.session.add(currency)
            db.session.add(self)
            db.session.add(purchase)
            db.session.commit()




db.create_all()


