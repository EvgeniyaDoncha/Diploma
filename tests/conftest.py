import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def base_api_url():
    return "https://reqres.in/api"


@pytest.fixture(scope="session")
def base_ui_url():
    return "https://www.python.org"


@pytest.fixture(scope="function")
def setup_browser(request):
    from selene.webdriver.chrome.options import Options
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "100.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)
    from selene.support import webdriver
    driver = webdriver.Remote(
        command_executor=f"https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options
    )

    from selene import Browser
    from selene import Config
    browser = Browser(Config(driver))
    yield browser


@pytest.hookimpl(hookwrapper=True)

def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    driver = item.funcargs.get("driver", None)
    if rep.when == "call" and rep.failed and driver:
        session_id = driver.session_id
        video_url = f"https://selenoid.autotests.cloud/video/{session_id}.mp4"

        try:
            allure.attach(driver.get_screenshot_as_png(),
                          name="screenshot",
                          attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass

        try:
            logs = driver.get_log("browser")
            log_text = "\n".join([f"{entry['level']} - {entry['message']}" for entry in logs])
            allure.attach(log_text, name="browser logs", attachment_type=allure.attachment_type.TEXT)
        except Exception:
            pass

        allure.attach(video_url, name="Video", attachment_type=allure.attachment_type.URI_LIST)