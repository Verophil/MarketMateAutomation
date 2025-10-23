from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class LoginPage(BasePage):
    # Input & Button
    EMAIL    = (By.XPATH, "//input[@type='email' or @placeholder='Email address']")
    PASSWORD = (By.XPATH, "//input[@type='password' or @placeholder='Password']")
    SIGN_IN  = (By.XPATH, "//button[normalize-space()='Sign In' or normalize-space()='Sign in']")

    # Logout
    LOGOUT_ANY = (By.XPATH,
        "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'logout') "
        "or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'log out')] "
        "| //a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'logout') "
        "or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'log out')]"
    )
    # Nav-Link „Shop“ in Header
    SHOP_LINK = (By.XPATH, "//a[normalize-space()='Shop']")

    # Error alert (fallback)
    ERROR_ALERT  = (By.XPATH, "//div[@role='alert' or contains(@class,'error')]")

    def login(self, email: str, password: str):
        WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(self.EMAIL))
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.SIGN_IN)

        WebDriverWait(self.driver, self.timeout).until(self._any_success_condition())

    def _any_success_condition(self):
        def _predicate(driver):
            try:
                if WebDriverWait(driver, 0.1).until(EC.visibility_of_element_located(self.LOGOUT_ANY)):
                    return True
            except Exception:
                pass
            try:
                if WebDriverWait(driver, 0.1).until(EC.visibility_of_element_located(self.SHOP_LINK)):
                    return True
            except Exception:
                pass
            if not driver.current_url.rstrip("/").endswith("/auth"):
                return True
            return False
        return _predicate

    def is_logged_in(self, timeout=5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: (
                    self._quick_visible(self.LOGOUT_ANY)
                    or self._quick_visible(self.SHOP_LINK)
                    or (not d.current_url.rstrip("/").endswith("/auth"))
                )
            )
            return True
        except Exception:
            return False

    def _quick_visible(self, locator):
        try:
            WebDriverWait(self.driver, 0.1).until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False

    def get_error_text(self, timeout=5) -> str:
        try:
            el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.ERROR_ALERT))
            return (el.text or "").strip()
        except Exception:
            return ""
