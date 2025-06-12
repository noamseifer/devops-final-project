from app import app, check_is_email


def test_check_is_email():
    assert check_is_email("abc@gmail.com") is True
    assert check_is_email("user.name+tag+sorting@example.com") is True
    assert check_is_email("plainaddress") is False
    assert check_is_email("missin_at_sign.com") is False
    assert check_is_email("missingdomain@.com") is False
    assert check_is_email("") is False


# def test_is_email_registered() -> None:
#     redis_client.delete("emails-set")
#     email = "test@example.com"
#     assert is_email_registered(email)  # True because not in redis
#     redis_client.sadd("emails-set", email)
#     assert not is_email_registered(email)  # False because now exists


# def test_main_page_returns_200():
#     with app.test_client() as client:
#         response = client.get("/")  # GET request to "/"
#         assert response.status_code == 200


# def test_emails_page_returns_200():
#     with app.test_client() as client:
#         response = client.get("/emails")  # GET request to "/emails"
#         assert response.status_code == 200
