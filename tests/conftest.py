import pytest
from sqlalchemy import create_engine
from server.wsgi import app as server_app, db


@pytest.fixture
def app():
    server_app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres@localhost:54320/task6_test'
    server_app.config['WTF_CSRF_ENABLED'] = False
    server_app.config['TESTING'] = True
    server_app.config['WTF_CSRF_ENABLED'] = False
    with server_app.app_context():
        db.create_all()
        yield server_app
        db.drop_all()


@pytest.fixture
def testing_db():
    return create_engine('postgresql://postgres@localhost:54320/task6_test')
