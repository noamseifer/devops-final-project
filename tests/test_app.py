from app import add, check_is_email

def test_add():
    assert add(2, 3) == 5


def test_check_is_email():
    assert check_is_email("abc@gmail.com") == True
    assert check_is_email("user.name+tag+sorting@example.com") == True
    assert check_is_email("plainaddress") == False
    assert check_is_email("missin_at_sign.com") == False
    assert check_is_email("missingdomain@.com") == False
    assert check_is_email("") == False


