import pytest


@pytest.fixture(scope='session')
def test_client(application):
    return application.test_client()
