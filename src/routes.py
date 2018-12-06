from flask import render_template, redirect, url_for, abort
from .forms import CompanySearchForm
from .models import Company, db
import requests as req
from . import app
import json


@app.route('/')
def home():
    """
    """
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def company_search():
    """Function for the company search. Accepts both the GET and POST methods
    """
    form = CompanySearchForm()

    if form.validate_on_submit():
        res = req.get(f'https://api.iextrading.com/1.0/stock/{ form.data["symbol"] }/company')

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
                'sector': data['sector'],
            }

            new_company = Company(**company)
            db.session.add(new_company)
            db.session.commit()

            return redirect(url_for('.portfolio_detail'))

        except json.JSONDecodeError:
            abort(404)

    return render_template('portfolio/search.html', form=form)


@app.route('/portfolio')
def portfolio_detail():
    """
    """
    return render_template('portfolio/portfolio.html')
