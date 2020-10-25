import pytest
from datastore.run import createApp


@pytest.fixture
def app():
    app = createApp("datastore.config")
    yield app
