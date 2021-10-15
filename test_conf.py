# import json
# import logging
# import os
# import joblib
import pytest
# from flask import Flask, url_for
# from flaskblog.main.routes import main
from flaskblog import create_app
# import tempfile
# from flask_sqlalchemy import SQLAlchemy
# from flaskblog import init_db
import os

# def test_Valid():
#     x=5
#     y=6
#     assert x==y

@pytest.fixture
def client():
    # db=SQLAlchemy()
    # db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True})
    #
    with app.test_client() as client:
        with app.app_context():
            # init_db()
            # db.init_app(app)
            yield client
    #
    # os.close(db_fd)
    # os.unlink(db_path)
    # app = create_app()
    # return app

def test_route(client):
#     app = create_app()
# #     app.register_blueprint(main,url_prefix='/')
#     web=app.test_client()
    rv=client.get('/about')
    print(rv)
    assert rv.status == '200 OK'

# def test_empty_db(client):
#     """Start with a blank database."""
#
#     rv = client.get('/')
#     assert rv.status == '200 OK'
    # assert b'No entries here so far' in rv.data
    # for i in rv.data:
    #     print('value in rv is :',i)
    # print('print rvdata:',rv.data)

# def test_app(client):
#     assert client.get(url_for('main.home')).status_code == 200

