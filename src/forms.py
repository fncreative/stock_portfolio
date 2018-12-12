from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CompanySearchForm(FlaskForm):
    """This allows for the searching of company stock by symbol"""
    symbol = StringField('symbol', validators=[DataRequired()])


class StockAddForm(FlaskForm):
    """This will allow for the addition of stock to the database"""
    symbol = StringField('symbol', validators=[DataRequired()])
