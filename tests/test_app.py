from app import check_is_email


def test_check_is_email():
    assert check_is_email("abc@gmail.com") == True
    assert check_is_email("user.name+tag+sorting@example.com") == True
    assert check_is_email("plainaddress") == False
    assert check_is_email("missin_at_sign.com") == False
    assert check_is_email("missingdomain@.com") == False
    assert check_is_email("") == False


