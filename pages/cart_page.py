import re
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    # --- Header / Navigation ---
    SHOP_LINK = (By.XPATH, "//a[normalize-space()='Shop']")
    # Cart-Icon: first clickable DIV, then Fallback SVG
    CART_ICON_DIV = (By.XPATH, "(//div[contains(@class,'headerIcon')])[last()]")
    CART_ICON_SVG = (By.XPATH, "(//svg[contains(@class,'headerIcon')])[last()]")

    PRODUCT_GRID = (By.XPATH, "//div[contains(@class,'product-grid')]")

    # --- List of products (Store) ---
    # first Add-to-Cart Button (class or text, case-insensitive)
    LIST_ADD_FIRST = (By.XPATH,
        "(//button[contains(@class,'btn-cart') or "
        "contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'add to cart')])[1]"
    )

    # --- Checkout-Container ---
    SHIPMENT_CONTAINER       = (By.XPATH, "//div[contains(@class,'shipment-container')]")
    PRODUCT_TOTAL_CONTAINER  = (By.XPATH, "//div[contains(@class,'product-total-container')]")
    TOTAL_CONTAINER          = (By.XPATH, "//div[contains(@class,'total-container')]")

    # --- Age-Verification Modal ---
    AGE_MODAL          = (By.XPATH, "//div[contains(@class,'modal-content')]")
    AGE_DOB_INPUT      = (By.XPATH, "//div[contains(@class,'modal-content')]//input[@placeholder='DD-MM-YYYY']")
    AGE_CONFIRM_BUTTON = (By.XPATH, "//div[contains(@class,'modal-content')]//button[normalize-space()='Confirm']")

    # ---------- internal helpers ----------
    def _maybe_handle_age_modal(self):
        """Wenn das Alters-Modal erscheint: mit Datum (>=18) bestätigen."""
        try:
            WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located(self.AGE_MODAL))
            dob = (datetime.today().replace(year=datetime.today().year - 20)).strftime("%d-%m-%Y")
            self.type(self.AGE_DOB_INPUT, dob)
            self.click(self.AGE_CONFIRM_BUTTON)
        except Exception:
            pass

    def _extract_euro_value(self, container_locator) -> float:
        """
        Liest aus dem Container-Text den letzten Euro-Betrag.
        Beispiel: "Product Total: 7.87€" -> 7.87
        """
        el = self.visible(container_locator)
        txt = el.text or ""
        # Suche nach Beträgen mit Euro-Zeichen
        matches = re.findall(r"([0-9]+(?:[.,][0-9]+)?)\s*€", txt)
        if not matches:
            # Fallback: irgendeine Zahl (falls € nicht im gleichen Node steht)
            matches = re.findall(r"([0-9]+(?:[.,][0-9]+)?)", txt)
        value_str = matches[-1] if matches else "0"
        return float(value_str.replace(",", ".").strip())

    # ---------- Aktionen ----------
    def open_shop(self):
        self.click(self.SHOP_LINK)

    def add_one_item_from_store_list(self):
        """Fügt aus der Store-Liste den ersten sichtbaren Artikel hinzu."""
        self._maybe_handle_age_modal()

        # Warte, bis das Grid da ist (Seite wirklich im Store)
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(self.PRODUCT_GRID)
        )

        # Warte nur auf Presence des Buttons (manche Seiten setzen Visibility erst spät)
        WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(self.LIST_ADD_FIRST)
        )

        # Klicken (scroll + JS-Fallback übernimmt BasePage.click)
        self.click(self.LIST_ADD_FIRST)

    def open_cart(self):
        """Öffnet den Warenkorb (Header-Icon)."""
        self.driver.execute_script("window.scrollTo(0, 0);")
        try:
            self.click(self.CART_ICON_DIV)
            return
        except Exception:
            self.click(self.CART_ICON_SVG)

    # ---------- Werte ----------
    def get_shipment(self) -> float:
        return self._extract_euro_value(self.SHIPMENT_CONTAINER)

    def get_product_total(self) -> float:
        return self._extract_euro_value(self.PRODUCT_TOTAL_CONTAINER)

    def get_total(self) -> float:
        return self._extract_euro_value(self.TOTAL_CONTAINER)
