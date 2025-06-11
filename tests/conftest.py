import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import os

@pytest.fixture(scope="session")
def base_api_url():
    return "https://reqres.in/api"  # пример тестового API

@pytest.fixture(scope="session")
def base_ui_url():
    return "https://www.python.org"  # тестовый сайт для UI

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless")  # без GUI
    options.add_argument("--window-size=1920,1080")

    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    driver.quit()
