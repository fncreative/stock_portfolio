from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CompanySearchForm(FlaskForm):
    """This allows for the searching of company stock by symbol"""
    symbol = StringField('symbol', validators=[DataRequired()])


class CompanyAddForm(FlaskForm):
    symbol = StringField('symbol', validators=[DataRequired()])
    companyName = StringField('companyName', validators=[DataRequired()])
    exchange = StringField('exchange', validators=[DataRequired()])
    industry = StringField('industry', validators=[DataRequired()])
    website = StringField('website', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    CEO = StringField('CEO', validators=[DataRequired()])
    issueType = StringField('issueType', validators=[DataRequired()])
    sector = StringField('sector', validators=[DataRequired()])

