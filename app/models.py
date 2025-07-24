from . import db
from flask_login import UserMixin
from datetime import datetime


class Vartotojas(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    el_pastas = db.Column(db.String(120), unique=True, nullable=False)
    slaptazodis = db.Column(db.String(60), nullable=False)


class Irasas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    suma = db.Column(db.Numeric(10, 2), nullable=False)
    pajamos = db.Column(db.Boolean, default=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    vartotojas_id = db.Column(db.Integer, db.ForeignKey('vartotojas.id'), nullable=False)


class Produktas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column(db.String(100), nullable=False)
    kaina = db.Column(db.Numeric(10, 2), nullable=False)
