import math
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.constants import (
    LOGIN_URL,
    FREE_SHIPPING_THRESHOLD,
    SHIPPING_FEE,
    VALID_USER,
)
from pages.cart_page import CartPage
from pages.login_page import LoginPage


def expected_shipping_for(total: float) -> float:
    """Rule: < 20 € => 5 €, sonst 0 €."""
    return 0.0 if total >= FREE_SHIPPING_THRESHOLD else SHIPPING_FEE


def test_shipping_rule_smoke(driver):
    # 1) Login
    driver.get(LOGIN_URL)
    LoginPage(driver).login(VALID_USER["email"], VALID_USER["password"])

    # Wait for "Shop"-Link and open Shop
    shop_link = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[normalize-space()='Shop']"))
    )
    shop_link.click()

    # Wait, for product-grid to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'product-grid')]"))
    )

    # 2) Add products until goal is reached
    cart = CartPage(driver)
    product_total = 0.0
    shipment = 0.0
    total = 0.0

    for _ in range(60):  # enough trials
        # 2.1 Add products
        cart.add_one_item_from_store_list()

        # 2.2 Open cart and read value
        cart.open_cart()
        product_total = cart.get_product_total()
        shipment = cart.get_shipment()
        total = cart.get_total()

        # Debug-Output
        print(f"[Cart] product_total={product_total:.2f}€, shipment={shipment:.2f}€, total={total:.2f}€")

        if product_total >= FREE_SHIPPING_THRESHOLD - 0.01:
            break

        # 2.3 Back to shop
        cart.open_shop()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'product-grid')]"))
        )

    # 3) Check shipment-rule
    assert math.isclose(
        shipment, expected_shipping_for(product_total), abs_tol=0.01
    ), f"Falsche Versandkosten: product_total={product_total:.2f}€, shipment={shipment:.2f}€"

    # 4) Plausibility check: Total == ProductTotal + Shipment
    assert math.isclose(
        total, product_total + shipment, abs_tol=0.01
    ), f"Total({total:.2f}) != ProductTotal({product_total:.2f}) + Shipment({shipment:.2f})"
