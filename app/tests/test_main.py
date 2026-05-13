"""
Unit tests for user management service
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app, validate_email

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_email_validation():
    """Test email validation - THIS TEST WILL FAIL"""
    # Valid emails should pass
    assert validate_email('user@example.com') == True
    assert validate_email('admin@company.org') == True
    
    # Invalid emails should fail
    assert validate_email('notanemail') == False
    assert validate_email('missing.at.symbol.com') == False  # FAILS: Bug allows this
    assert validate_email('@nodomain.com') == False
    assert validate_email('user@') == False

def test_create_user_valid(client):
    """Test user creation with valid data"""
    response = client.post('/users', 
                          json={'email': 'test@example.com', 'username': 'testuser'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User created successfully'

def test_create_user_invalid_email(client):
    """Test user creation with invalid email"""
    response = client.post('/users', 
                          json={'email': 'invalid-email', 'username': 'testuser'})
    assert response.status_code == 400

def test_create_user_short_username(client):
    """Test user creation with too short username"""
    response = client.post('/users', 
                          json={'email': 'test@example.com', 'username': 'ab'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'Username must be at least 3 characters' in data['error']
