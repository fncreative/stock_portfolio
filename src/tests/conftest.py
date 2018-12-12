import os
import tempfile

from src import app
from src.models import db, Company

import pytest

@pytest.fixture
def client():

    def do_nothing():
        pass

    db.session.commit = do_nothing

    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    yield app.test_client()

    db.session.rollback()
