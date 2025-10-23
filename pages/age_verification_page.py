from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class AgeVerificationPage(BasePage):
    # Modal that asks for DOB
    MODAL = (
        By.XPATH,
        "//div[contains(@class,'modal') and .//input[@placeholder='DD-MM-YYYY']]"
        " | //div[contains(@class,'modal-content')][.//input[@placeholder='DD-MM-YYYY']]"
    )

    # DOB input
    DOB_INPUT = (
        By.XPATH,
        "//input[@placeholder='DD-MM-YYYY' or @name='dob' or contains(@id,'dob')]"
    )

    # Confirm button inside the modal
    CONFIRM_BTN = (
        By.XPATH,
        "(//div[contains(@class,'modal') or contains(@class,'modal-content')]"
        "//button[normalize-space()='Confirm' or contains(.,'Confirm')])[last()]"
    )

    # Underage/info toast:
    TOAST = (
        By.XPATH,
        "(//div[@role='status' and @aria-live='polite'])[last()]"
    )

    # Evidence that the modal closed
    STORE_GRID = (
        By.XPATH,
        "//div[contains(@class,'product-grid') or @data-testid='product-grid']"
    )

    # ---------- Actions ----------
    def wait_for_modal(self, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.MODAL)
        )

    def enter_dob(self, dob: str):
        self.type(self.DOB_INPUT, dob)

    def submit(self):
        self.click(self.CONFIRM_BTN)

    def verify_age(self, dob: str):
        # be defensive in case caller forgets to wait explicitly
        try:
            self.wait_for_modal(timeout=5)
        except Exception:
            pass
        self.enter_dob(dob)
        self.submit()

    # ---------- Assertions / getters ----------
    def modal_is_closed(self, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.MODAL)
            )
            return True
        except Exception:
            # accept store grid visible as “closed” too
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located(self.STORE_GRID)
                )
                return True
            except Exception:
                return False

    def get_error_message(self, timeout: int = 4) -> str | None:
        try:
            el = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.TOAST)
            )
            # Wait up to ~1s for text to actually fill in (these live regions can be late)
            WebDriverWait(self.driver, 1).until(
                lambda d: (el.text or "").strip() != ""
            )
            text = (el.text or "").strip()
            return text or None
        except Exception:
            return None
