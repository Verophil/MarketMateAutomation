import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.constants import NON_ALCOHOL_PRODUCT_URL, LOGIN_URL, VALID_USER
from pages.login_page import LoginPage
from pages.rating_page import RatingPage

def _login(driver):
    driver.get(LOGIN_URL)
    LoginPage(driver).login(VALID_USER["email"], VALID_USER["password"])
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Shop']"))
    )

def test_rating_requires_purchase(driver):
    """EP: rating without purchase is not possible (gate message visible)."""
    _login(driver)
    driver.get(NON_ALCOHOL_PRODUCT_URL)

    page = RatingPage(driver)
    page.wait_loaded()

    assert page.has_purchase_gate(), (
        "Expected purchase gate on product page, but it was not found. "
        "This test verifies the 'cannot rate without purchase' rule."
    )

@pytest.mark.xfail(reason="Site requires a real purchase before rating; kept for documentation.")
@pytest.mark.parametrize("stars, feedback", [
    (1, ""),
    (5, ""),
    (3, "a" * 500),
    (4, "a" * 501),  # would expect 'Feedback cannot exceed 500 characters'
])
def test_rating_happy_paths_blocked_without_purchase(driver, stars, feedback):
    """Document the intended scenarios but xfail because purchase is required."""
    _login(driver)
    driver.get(NON_ALCOHOL_PRODUCT_URL)

    page = RatingPage(driver)
    page.wait_loaded()

    # This will remain blocked by the purchase gate on the real site.
    assert not page.has_purchase_gate(), "Rating stays blocked without purchase."
