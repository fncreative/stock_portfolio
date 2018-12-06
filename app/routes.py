from . import app

# 3rd Party Requirements
from flask import render_template, abort, redirect, url_for, session, g, make_response
from sqlalchemy.exc import IntegrityError

# Models
from .models import db, Stock

# Forms
from .forms import StockSearchForm

# API Requests & Other
import json
from json import JSONDecodeError
import requests as req
import os


# Helpers
def fetch_stock_data(company):
    return req.get(f'https://api.iextrading.com/1.0/stock/{company}/company')


# Controllers #
@app.route('/')
def home():
    """Base route, renders basic home page with minimal content"""
    return render_template('home.html', msg='Welcome')


@app.route('/search', methods=['GET', 'POST'])
def stock_search():
    form = StockSearchForm()

    if form.validate_on_submit():
        try:
            res = fetch_stock_data(form.data['company'])
            session['context'] = res.text

        except JSONDecodeError:
            abort(404)

        return redirect(url_for('.portfolio'))

    return render_template('search.html', form=form)


@app.route('/portfolio')
@app.route('/portfolio/<company_name>')
def portfolio(company_name=None):

    try:
        if company_name:
            res = fetch_stock_data(company_name)
            return render_template('portfolio.html', company_data=res)

        context = json.loads(session['context'])
        return render_template('portfolio.html', company_data=context)

    except JSONDecodeError:
            abort(404)
