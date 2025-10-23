import pytest
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.constants import LOGIN_URL, VALID_USER
from pages.login_page import LoginPage
from pages.age_verification_page import AgeVerificationPage


def _adult_dob_str(years=19) -> str:
    today = date.today()
    return today.replace(year=today.year - years).strftime("%d-%m-%Y")

def _underage_dob_str(years=17) -> str:
    today = date.today()
    return today.replace(year=today.year - years).strftime("%d-%m-%Y")


# Known flaky/buggy validations -> mark as xfail (will show XPASS if app fixes them)
xfail_empty   = pytest.mark.xfail(reason="App often lacks 'required' toast for empty DOB", strict=False)
xfail_format  = pytest.mark.xfail(reason="App often lacks 'invalid format' toast", strict=False)
xfail_unreal  = pytest.mark.xfail(reason="App often lacks 'invalid date' toast", strict=False)


@pytest.mark.parametrize(
    "dob, expected_message",
    [
        (_adult_dob_str(), None),  # adult → expect no error toast
        (_underage_dob_str(),
         "You are underage. You can still browse the site, but you will not be able to view alcohol products."),
        pytest.param("", "Date of Birth is required.", marks=xfail_empty),
        pytest.param("13/25/2008", "Invalid Date of Birth format. Please use DD-MM-YYYY.", marks=xfail_format),
        pytest.param("01-01-1875", "Please enter a valid date of birth.", marks=xfail_unreal),
    ],
    ids=["adult_ok", "underage_toast", "empty_required", "format_invalid", "unrealistic_invalid"],
)
def test_age_verification(driver, dob, expected_message):
    # 1) Login
    driver.get(LOGIN_URL)
    LoginPage(driver).login(VALID_USER["email"], VALID_USER["password"])

    # 2) Go to Shop (age modal appears here)
    shop_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Shop']"))
    )
    shop_link.click()

    # 3) Interact with age modal
    age = AgeVerificationPage(driver)
    age.wait_for_modal()
    age.verify_age(dob)

    # 4) Assertions
    if expected_message is None:
        # Modal muss zugehen
        assert age.modal_is_closed(), "Age modal should close for a valid adult DOB."

        # The app shows (actually) a success toast. Accept both:
        # no toast (ideal behavior)
        # or success toast with 'You are of age'
        msg = age.get_error_message()
        if msg:  # if a toast shows up, it should be a success toast
            assert "You are of age" in msg, f"Unexpected toast for valid DOB: {msg!r}"
    else:
        msg = age.get_error_message()
        assert msg, "Expected an error toast, but none was found."
        assert expected_message in msg, f"Expected toast to contain: {expected_message!r}, got: {msg!r}"
