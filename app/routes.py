from . import app
from flask import render_template, abort, redirect, url_for, session, g, make_response
from sqlalchemy.exc import IntegrityError
from .models import db, Company
from .forms import StockSearchForm
import json
from json import JSONDecodeError
import requests as req
import os


# Controllers #
@app.route('/')
def home():
    """Base route, renders basic home page with minimal content"""
    return render_template('home.html', msg='Welcome')


@app.route('/search', methods=['GET', 'POST'])
def stock_search():
    """Search for company stock information."""
    form = StockSearchForm()

    if form.validate_on_submit():
        res = req.get(f'https://api.iextrading.com/1.0/stock/{ form.data[0] }/company')

        try:
            data = json.loads(res.text)
            company = {
                'symbol': data['symbol'],
                'companyName': data['companyName'],
                'exchange': data['exchange'],
                'industry': data['industry'],
                'website': data['website'],
                'description': data['description'],
                'CEO': data['CEO'],
                'issueType': data['issueType'],
                'sector': data['sector']
            }

            new_company = Company(**company)
            db.sessoin.add(new_company)
            db.session.commit()

            return redirect(url_for('.portfolio'))

        except json.JSONDecodeError:
            abort(404)


    return render_template('search.html', form=form)


@app.route('/portfolio')
def portfolio_detail():

    return render_template('portfolio/portfolio_detail.html')

