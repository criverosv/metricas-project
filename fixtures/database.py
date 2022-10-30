import pytest
from ..models import db as db_


@pytest.fixture(autouse=True)
def db(application):
    '''
    Session-wide test database.
    '''
    db_.app = application
    db_.create_all()
    yield db_
    db_.drop_all()
