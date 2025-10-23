from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

class RatingPage(BasePage):
    PURCHASE_GATE = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'You need to buy this product to tell us your opinion')]"
    )

    PRODUCT_TITLE = (By.XPATH, "//h1 | //h2 | //h3[contains(@class,'title') or contains(., '')]")

    def wait_loaded(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(self.PRODUCT_TITLE)
        )

    def has_purchase_gate(self) -> bool:
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.PURCHASE_GATE)
            )
            return True
        except Exception:
            return False
