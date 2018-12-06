from . import app

# DB-Related Imports
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime as dt

db = SQLAlchemy(app)
migrate = Migrate(app,db)

# Models #


class Stock(db.Model):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(256), index=True, unique=True)
    date_created = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        return '<Stock {}>'.format(self.companyName)
