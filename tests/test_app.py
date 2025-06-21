from unittest.mock import MagicMock
from app import app, check_is_email, redis_client


def test_check_is_email():
    assert check_is_email("abc@gmail.com") is True
    assert check_is_email("user.name+tag+sorting@example.com") is True
    assert check_is_email("plainaddress") is False
    assert check_is_email("missin_at_sign.com") is False
    assert check_is_email("missingdomain@.com") is False
    assert check_is_email("") is False


def test_is_email_registered(monkeypatch):
    mock_redis = MagicMock()
    monkeypatch.setattr(app, "redis_client", mock_redis)
    email = "test@example.com"
    # First call: not in Redis
    mock_redis.sismember.return_value = False
    assert is_email_registered(email) is True

    # Now simulate email is in Redis
    mock_redis.sismember.return_value = True
    assert is_email_registered(email) is False



def test_main_page_returns_200(monkeypatch):
    mock_redis = MagicMock()
    monkeypatch.setattr(app, "redis_client", mock_redis)
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200


def test_emails_page_returns_200(monkeypatch):
    mock_redis = MagicMock()
    monkeypatch.setattr(app, "redis_client", mock_redis)

    with app.test_client() as client:
        response = client.get("/emails")
        assert response.status_code == 200