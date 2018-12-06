from . import app

#DB-Related Imports
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from passlib.hash import pbkdf2_sha256 as pass_hash

from datetime import datetime as dt

db = SQLAlchemy(app)
migrate = Migrate(app,db)

# Models #

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    stockName = db.Column(db.String(256), index=True, unique=True)
    date_created = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        return '<Stock {}>'.format(self.stockName)
