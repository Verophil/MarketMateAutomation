from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def find(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def visible(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def click(self, locator):
        el = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        try:
            el.click()
        except Exception:
            # Fallback for Overlay
            self.driver.execute_script("arguments[0].click();", el)

    def type(self, locator, text):
        el = self.visible(locator)
        el.clear()
        el.send_keys(text)
