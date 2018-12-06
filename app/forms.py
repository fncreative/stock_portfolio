#Flask-WTF Forms
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


# Form #

class StockSearchForm(FlaskForm):
    """Form that allows for the search of the stock"""
    stock_name = StringField('name', validators=[DataRequired()])
