from flask import session
import pytest
from .. import app
from src.models import db


@pytest.fixture
def client():
    def do_nothing():
        pass
    db.session.commit = do_nothing
    yield app.test_client()
    db.session.rollback()


def test_home_get():
    """Test the home route and code"""
    rv = app.test_client().get('/')
    assert rv.status_code == 200


def test_home_get_content():
    """Test the home route to get data"""
    rv = app.test_client().get('/')
    assert b'<h1>Welcome to the site</h1>' in rv.data


def test_home_method_nonexist():
    """Test a method that doesnt exist"""
    rv = app.test_client().delete('/')
    assert rv.status_code == 405


def test_search_route():
    """Test the search method"""
    rv = app.test_client().get('/search')
    assert rv.status_code == 200


def test_search_get_content():
    """Test the search method for content"""
    rv = app.test_client().get('/search')
    assert b'<h2>Search for a stock symbol</h2>' in rv.data


def test_search_incorrect_method():
    """Test for a method that does not exist in search"""
    rv = app.test_client().delete('/search')
    assert rv.status_code == 405


def test_search_route_post(client):
    """Test the search route post method"""
    rv = client.post('/search', data={'symbol': 'goog'})
    assert rv.status_code == 200


def test_portfolio_route(client):
    """Test that the portfolio page exists"""
    rv = client.get('/portfolio')
    assert rv.status_code == 200


def test_portfolio_content():
    """Test that content can be received"""
    rv = app.test_client().get('/portfolio')
    assert b'<p>Microsoft Corporation (MSFT)</p>' in rv.data


def test_portfolio_content_error():
    """Test that an incorrect route generates a 404"""
    rv = app.test_client().get('/qwerty')
    assert rv.status_code == 404


def test_404():
    """Test the final 404 error"""
    rv = app.test_client().get('/qwerty')
    assert b'<h1>404 - Page Not Found</h1>' in rv.data
