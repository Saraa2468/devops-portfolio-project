from app.app import app
import json

def test_index():
    client = app.test_client()
    resp = client.get('/')
    data = json.loads(resp.data)
    assert 'message' in data

def test_health():
    client = app.test_client()
    resp = client.get('/health')
    data = json.loads(resp.data)
    assert data['status'] == 'ok'
