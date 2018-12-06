from . import app

# 3rd Party Requirements
from flask import render_template, abort, redirect, url_for, session, g, make_response
from sqlalchemy.exc import IntegrityError

# Models
from .models import db, Stock

#Forms
from .forms import StockSearchForm

# API Requests & Other
from json import JSONDecodeError
import requests as req
import json
import os

# helpers
def fetch_stock_price(stock):
    return req.get(f"{os.getenv('API_URL')}{stock}&APPID={os.getenv('API_URL')}")

# Controllers #
@app.route('/')
def home():
    """Base route, renders basic home page with minimal content"""
    return render_template('home.html', msg='Welcome')

@app.route('/search', methods=['GET', 'POST'])
def stock_search():
    """Proxy endpoint for retrieveing stock information from 3rd party"""
    form = StockSearchForm()

    if form.validate_on_submit():
        stock = form.data['stock_name']

        res = fetch_stock_price(stock)

        try:
            session['context'] = res.next
            return redirect(url_for('.stock_detail'))

        except JSONDecodeError:
            abort(404)

    return render_template('search.html', form=form)

@app.route('/stock')
@app.route('/stock/<stock_name>')
def stock_detail(stock_name = None):

    if stock_name:
        res = fetch_stock_price(stock_name)
        return render_template('stock_detail.html', **res.json())

    else:

        try:
            context - json.loads(session['context'])
            stock = Stock(stockName = context['name'])
            print('stock', stock)
            db.session.add(stock)
            db.session.commit()
            return render_template('stock_detail.html', **context)
        except IntegrityError as e:
            print(e)
            res = make_response('That stock has already been added', 400)
            return res
