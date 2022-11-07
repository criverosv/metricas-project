import pytest
from flask import Flask
from ..models import db as db_


@pytest.fixture(scope='session')
def application():
    app = Flask('test')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profile_test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'clave-jwt'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['SERVER_NAME'] = 'localhost'
    db_.init_app(app)
    app_context = app.app_context()
    app_context.push()

    from urls import register_routes
    register_routes(app)

    yield app
    app_context.pop()
