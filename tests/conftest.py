import pytest
from tickr.server import main as tickr_app


@pytest.fixture(scope='session')
def app():
    return tickr_app
    