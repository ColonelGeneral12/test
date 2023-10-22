from app.calculations import add, subtract, divide, multiply, BankAccount
import pytest

@pytest.fixture                 # This is a fixture that enables time saving
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def new_bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (12, 3, 15),
    (100, 20, 120),
    (7, 5, 12)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(8, 4) == 4


def test_multiply():
    assert multiply(6, 3) == 18


def test_divide():
    assert divide(81, 9) == 9


def test_bank_default_amount(new_bank_account):
    assert new_bank_account.balance == 50


def test_bank_initial_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(new_bank_account):
    new_bank_account.withdraw(20)
    assert new_bank_account.balance == 30


def test_deposit(new_bank_account):
    new_bank_account.deposit(100)
    assert new_bank_account.balance == 150


def test_collect_intrest(new_bank_account):
    new_bank_account.collect_interest()
    assert round(new_bank_account.balance, 6) == 55

def test_transactions(zero_bank_account):
    zero_bank_account.deposit(200)
    zero_bank_account.withdraw(100)
    assert zero_bank_account.balance == 100