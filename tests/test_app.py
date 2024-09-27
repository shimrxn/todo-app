import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert b'To-Do List' in rv.data

def test_add_delete_task(client):
    rv = client.post('/add', data=dict(task='Test Task'), follow_redirects=True)
    assert b'Test Task' in rv.data

    rv = client.get('/delete/1', follow_redirects=True)
    assert b'Test Task' not in rv.data
