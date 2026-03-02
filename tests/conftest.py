import os
import tempfile
import pytest
from habithub import create_app, db as _db, cache as _cache
from habithub.auth import API_KEY

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    application = create_app()
    application.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    application.config["TESTING"] = True
    application.config["CACHE_TYPE"] = "SimpleCache"

    with application.app_context():
        _db.create_all()
        yield application
        _cache.clear()
        _db.session.remove()
        _db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Return a test client that sends the API key header with every request."""
    test_client = app.test_client()
    test_client.environ_base["HTTP_X_API_KEY"] = API_KEY
    return test_client
