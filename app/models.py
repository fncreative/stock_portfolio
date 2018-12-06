from . import app

# DB-Related Imports
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime as dt

db = SQLAlchemy(app)
migrate = Migrate(app,db)


class Company(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(64), index=True, unique=True)
    companyName = db.Column(db.String(256), index=True, unique=True)
    exchange = db.Column(db.String(128))
    industry = db.Column(db.String(128))
    website = db.Column(db.String(128))
    description = db.Column(db.String(128))
    CEO = db.Column(db.String(128))
    issueType = db.Column(db.String(128))
    sector = db.Column(db.String(128))

    def __repr__(self):
        return '<Stock {}>'.format(self.companyName)
