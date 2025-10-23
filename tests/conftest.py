import os
import sys
import pytest
from selenium import webdriver


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    from utils.constants import LOGIN_URL
    from pages.login_page import LoginPage

    driver.get(LOGIN_URL)
    return LoginPage(driver)


@pytest.fixture
def store_ready(driver):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'product-grid')]"))
    )
    return driver
