import pytest
from src.app import app

def test_health_endpoint():
    with app.test_client() as client:
        response = client.get('/api/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'

def test_login_with_valid_credentials():
    with app.test_client() as client:
        response = client.post('/api/login', json={'password': 'secure_password_123'})
        assert response.status_code == 200
        assert response.json['status'] == 'success'

def test_login_with_invalid_credentials():
    with app.test_client() as client:
        response = client.post('/api/login', json={'password': 'wrong_password'})
        assert response.status_code == 401
