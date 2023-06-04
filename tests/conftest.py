import os
import tempfile

import pytest
from src import create_app 
from src.database import db
    
@pytest.fixture
def app():
    app = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db', 'JWT_SECRET_KEY': 'JWT_SECRET_KEY'})
    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()