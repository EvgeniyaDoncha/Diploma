import allure
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

    SELENOID_URL = "https://user1:1234@selenoid.autotests.cloud/wd/hub"  # замени на свой URL

    @pytest.fixture(scope="function")
    def driver(request):
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "115.0",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
            }
        }
        driver = webdriver.Remote(command_executor=SELENOID_URL, desired_capabilities=capabilities)
        yield driver
        driver.quit()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        # Получаем результат теста
        outcome = yield
        rep = outcome.get_result()

        driver = item.funcargs.get("driver", None)

        if driver:
            session_id = driver.session_id
            video_url = f"http://selenoid.yourdomain.com:4444/video/{session_id}.mp4"

        if rep.when == "call" and rep.failed and driver:
            allure.attach(driver.get_screenshot_as_png(),
                          name="screenshot",
                          attachment_type=allure.attachment_type.PNG)
            try:
                logs = driver.get_log('browser')
                log_text = "\n".join([f"{entry['level']} - {entry['message']}" for entry in logs])
                allure.attach(log_text, name="browser logs", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                print(f"Не удалось получить логи браузера: {e}")

            allure.attach(video_url,
                          name="Video",
                          attachment_type=allure.attachment_type.URI_LIST)

    # Вставляй этот код в конец своего conftest.py, не удаляя остального.
