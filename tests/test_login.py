import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.constants import VALID_USER, INVALID_USER, ERROR_INVALID_LOGIN


def test_login_valid(driver, login_page):
    # Act
    login_page.login(VALID_USER["email"], VALID_USER["password"])

    # Assert: logged in
    assert login_page.is_logged_in(), "Login should succeed, but Logout button was not found."


@pytest.mark.parametrize("email,password,expected_error", [
    (INVALID_USER["email"], INVALID_USER["password"], ERROR_INVALID_LOGIN),
    ("", INVALID_USER["password"], ERROR_INVALID_LOGIN),
    (INVALID_USER["email"], "", ERROR_INVALID_LOGIN),
])
def test_login_invalid(driver, login_page, email, password, expected_error):
    # Act
    login_page.login(email, password)

    # Assert: Error message visible
    actual = (login_page.get_error_text() or "").lower()
    expected = (expected_error or "").lower()
    assert expected in actual, f"Expected error '{expected_error}', but got '{actual}'"
