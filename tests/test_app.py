import sys
import os

# Add the src folder to sys.path so Python can find app.py inside src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import app as app_module
from app import app, check_is_email, is_email_registered
from unittest.mock import MagicMock


def test_check_is_email():
    assert check_is_email("abc@gmail.com") is True
    assert check_is_email("user.name+tag+sorting@example.com") is True
    assert check_is_email("plainaddress") is False
    assert check_is_email("missin_at_sign.com") is False
    assert check_is_email("missingdomain@.com") is False
    assert check_is_email("") is False


def test_is_email_registered(monkeypatch):
    mock_redis = MagicMock()
    monkeypatch.setattr(app_module, "redis_client", mock_redis)
    email = "test@example.com"
    
    mock_redis.sismember.return_value = False
    assert is_email_registered(email) is False

    mock_redis.sismember.return_value = True
    assert is_email_registered(email) is True



def test_main_page_returns_200(monkeypatch):
    mock_redis = MagicMock()
    monkeypatch.setattr(app_module, "redis_client", mock_redis)
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200


def test_emails_page_returns_200(monkeypatch):
    mock_redis = MagicMock()
    monkeypatch.setattr(app_module, "redis_client", mock_redis)

    with app.test_client() as client:
        response = client.get("/emails")
        assert response.status_code == 200


def test_metrics_endpoint_returns_200():
    with app.test_client() as client:
        response = client.get("/metrics")
        assert response.status_code == 200
